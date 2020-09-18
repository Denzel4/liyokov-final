from datetime import datetime
import logging
import logging.config
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user
import numpy as np
import random
import glob
import os, time, json
from PIL import Image
from flask_cors import CORS
from itertools import *
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, Lambda, Conv2D, MaxPooling2D, Activation
from tensorflow.keras.optimizers import RMSprop
import argparse
import nvidia_smi
import math
import psutil
import logging




AUTOTUNE = tf.data.experimental.AUTOTUNE
CONFIG_FILE = 'config_SC.json'
MEM_PER_MODEL = 10000

def get_AI_manager_details(config_dict):
	config_dict["CPU"] = psutil.cpu_percent()
	config_dict["RAM"]  = psutil.Process(os.getpid()).memory_info()[0]/2.**30
	return config_dict


#Loss Function of the model
def contrastive_loss(y_true, y_pred):
    """Contrastive loss from Hadsell-et-al.'06
    http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
    """
    margin = 1
    square_pred = tf.square(y_pred)
    margin_square = tf.square(tf.maximum(margin - y_pred, 0))
    return tf.reduce_mean(y_true * square_pred + (1 - y_true) * margin_square)

#Data Generator Class
class Data_Generator(object):
    #Keep everything as it is. We can not change most of the static values. 
    #Keep batch size always 1 - In this generator it indicates that we will read ONE inference image
    #The actual batch size as input the model is equalt to Number of Images under gold_dir. 
    def __init__(self, query_img_name_list, ref_img_array, input_shape):
        print('Initiating Data Pipeline')
        self.query_img_name_list = query_img_name_list
        self.ref_img_array = tf.convert_to_tensor(ref_img_array)
        self.input_shape = input_shape
        self.total_sample = len(self.query_img_name_list)
        self.total_ref_sample = self.ref_img_array.shape[0]
        self.row_to_col_ratio = self.input_shape[0] / self.input_shape[1]
        if self.row_to_col_ratio >= 1:
            self.orientation = "Portrait"
        else:
            self.orientation = "Landscape"


    def get_img_file(self, img_name):
        ip_img = tf.io.read_file(img_name)
        #que_img_str = tf.io.encode_base64(ip_img, pad=True)
        que_img = tf.image.decode_jpeg(ip_img, channels=3)
        que_img = tf.image.resize(que_img, [self.input_shape[0], self.input_shape[1]])
        que_img = tf.cast(que_img, tf.float32)/255.0
        return que_img, img_name
    
    def get_arrays(self, que_img, img_name):
        que_img_array = tf.tile(que_img, [tf.shape(self.ref_img_array)[0], 1, 1, 1])
        return {'input_2':que_img_array, 'input_3':self.ref_img_array, 'filename':img_name}

    def get_dataset(self):
        with tf.device('/cpu:0'):
            dataset = tf.data.Dataset.from_tensor_slices(np.asarray(self.query_img_name_list))
            dataset = dataset.shuffle(len(self.query_img_name_list))
            dataset = dataset.map(self.get_img_file, num_parallel_calls=AUTOTUNE)
            dataset = dataset.batch(1, drop_remainder=True) #We can not try any other batch size apart from 1.
            dataset = dataset.map(self.get_arrays, num_parallel_calls=AUTOTUNE)
            dataset = dataset.prefetch(buffer_size=1)
        return dataset

#Function to Read images from list of image names and store them in one numpy array
#Used to store the Array of Reference Images
def get_array_from_img_list(img_name_list, input_shape):
    img_list = []
    for img_name in img_name_list:
        img_list.append(np.array(Image.open(img_name).resize((input_shape[1], input_shape[0]))))
    img_array = np.asarray(img_list).astype("float32")
    img_array /= 255.0
    return img_array

#Function to get dictionry of paths for weights files.
#The key of dictiory is cameras ID
def get_weight_file_path_dict(config_dict, data_dir):
    weight_file_path_dict = {}
    for key in config_dict.keys():
        weight_file_path_dict[key] = os.path.join(data_dir,key,config_dict[key]['weight_file'])
    return weight_file_path_dict

#Function to get dictionry of loaded models.
#The key of dictiory is cameras ID
def get_and_load_models(weight_file_path_dict, logical_devices_dict):
    model_dict = {}
    for key in weight_file_path_dict.keys():
        print(weight_file_path_dict[key])
        with tf.device(logical_devices_dict[key]):
            model_dict[key] = load_model(weight_file_path_dict[key], custom_objects={'contrastive_loss': contrastive_loss})
        print("Models {} loaded on {}".format(weight_file_path_dict[key], logical_devices_dict[key]))
    return model_dict

#Function to get dictionry of data generators.
#The key of dictiory is cameras ID
def get_datagenrator_dict(config_dict, data_dir):
    data_generator_dict = {}
    for key in config_dict.keys():
        ref_img_dir = os.path.join(data_dir, key, 'Train')
        inf_img_dir = os.path.join(data_dir, key, 'Inference_images')
        ref_img_name_list = [os.path.join(ref_img_dir, x) for x in os.listdir(ref_img_dir) if x.lower().endswith(('.jpg', '.jpeg', 'JPEG'))]
        ref_img_array = get_array_from_img_list(img_name_list=ref_img_name_list, input_shape=config_dict[key]['ImageSize(H,W,C)'])
        inf_img_name_list = [os.path.join(inf_img_dir, x) for x in os.listdir(inf_img_dir) if x.lower().endswith(('.jpg', '.jpeg', 'JPEG'))]
        data_generator_dict[key] = Data_Generator(query_img_name_list=inf_img_name_list, ref_img_array=ref_img_array, input_shape=config_dict[key]['ImageSize(H,W,C)'])
    return data_generator_dict  

#Read and convert image to base64 encoding
def read_img_base64(ip_filename, ip_shape):
    image = Image.open(ip_filename)
    image = image.resize((ip_shape[1], ip_shape[0]), Image.ANTIALIAS)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    decoded_image = buffered.getvalue()
    img_str = base64.b64encode(decoded_image)
    return img_str

#Run the inference on single image.
def run_inference_on_one_image(image_batch, base_model, threshold, num_ref_images, camera_ID, orientation, ip_shape):
    pred_dict = {}
    batch_label = True
    y_pred = base_model.predict(image_batch, verbose=1)
    prediction_array = np.where(y_pred > threshold, 1, 0)
    uniquevalue, freq = np.unique(prediction_array, return_counts=True)
    freq_list = freq.tolist()
    uniquevalue_list = uniquevalue.tolist()
    index_to_check = freq_list.index(max(freq_list))
    confidence = (max(freq_list) / num_ref_images) * 100
    similarity_score = uniquevalue_list[index_to_check]

    if similarity_score == 0:
        pred_dict["label"] = "OK"
    elif similarity_score == 1:
        pred_dict["label"] = "NG"
        batch_label = False

    pred_dict["confidence"] = confidence
    pred_dict["base64"] = read_img_base64(image_batch['filename'].numpy()[0], ip_shape=ip_shape).decode('utf-8')
    pred_dict["filename"] = image_batch['filename'].numpy()[0].decode('utf-8')
    pred_dict["camera_ID"] = camera_ID
    pred_dict["batch_result"] = batch_label
    pred_dict["orientation"] = orientation

    return pred_dict

def get_free_gpu_memories(gpu_index):
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(gpu_index)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    free_mem = math.floor((info.free * 9.3132e-10)*1073)
    return free_mem

def physical_devices_list_to_dict(physical_devices_list):
    physical_devices_dict = {}
    for i in range(len(physical_devices_list)):
        physical_devices_dict[physical_devices_list[i][0]] = {'device':physical_devices_list[i], 'index':i}
    return physical_devices_dict

def get_device_to_model_map(gpu_dict, cpu_dict, model_list, memory_per_model):
    logical_devices_dict = {}
    gpus_to_model_map_dict = {}
    cpus_to_model_map_dict = {}
    all_models_on_gpu = []
    all_models_on_cpu = []
    model_list_counter = 0
    total_models = len(model_list)
    if gpu_dict:
        for key in gpu_dict.keys():
            gpu_device = gpu_dict[key]['device']
            gpu_index = gpu_dict[key]['index']
            gpu_free_mem = get_free_gpu_memories(gpu_index)
            total_models_on_device = math.floor(gpu_free_mem/memory_per_model)
            print("Device {} will have {} Models".format(key, total_models_on_device))
            model_ids = model_list[model_list_counter:model_list_counter+total_models_on_device]
            gpus_to_model_map_dict[key] = model_ids
            all_models_on_gpu += model_ids
            model_list_counter += total_models_on_device
        if model_list_counter < total_models:
            key = list(cpu_dict.keys())[0]
            cpu_device = cpu_dict[key]['device']
            cpu_index = cpu_dict[key]['index']
            model_ids = model_list[model_list_counter:total_models]
            cpus_to_model_map_dict[key] = model_ids
            all_models_on_cpu += model_ids
    else:
        key = list(cpu_dict.keys())[0]
        cpu_device = cpu_dict[key]['device']
        cpu_index = cpu_dict[key]['index']
        model_ids = model_list[model_list_counter:total_models]
        cpus_to_model_map_dict[key] = model_ids
        all_models_on_cpu += model_ids

    if gpu_dict:
        for key in gpus_to_model_map_dict.keys():
            virtual_gpu_list = [tf.config.LogicalDeviceConfiguration(memory_per_model) for i in range(len(gpus_to_model_map_dict[key]))]
            tf.config.set_logical_device_configuration(gpu_dict[key]['device'], virtual_gpu_list)
    if cpu_dict:
        for key in cpus_to_model_map_dict.keys():
            virtual_cpu_list = [tf.config.LogicalDeviceConfiguration() for i in range(len(cpus_to_model_map_dict[key]))]
            tf.config.set_logical_device_configuration(cpu_dict[key]['device'], virtual_cpu_list)


    if gpu_dict:
        logical_gpus = tf.config.list_logical_devices('GPU')
        for i in range(len(logical_gpus)):
            logical_devices_dict[all_models_on_gpu[i]] = logical_gpus[i]
    
    logical_cpus = tf.config.list_logical_devices('CPU')
    for i in range(len(logical_cpus)):
        logical_devices_dict[all_models_on_cpu[i]] = logical_cpus[i]

    return logical_devices_dict