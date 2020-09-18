'''
from project.server.handlers.database.monitoring import next_inference, calendar, select_all_inference
from project.server.inference.inference_result import *
import tensorflow as tf
import json

AUTOTUNE = tf.data.experimental.AUTOTUNE
CONFIG_FILE = 'config_SC.json'
MEM_PER_MODEL = 10000

with open(CONFIG_FILE) as f:
    config = json.load(f)
CONFIG_DICT = config['InferenceDetails']
DATA_DIR = config['DATA_DIR']
CAMERA_LIST = list(CONFIG_DICT.keys())
print("Found {} Cameras in {}".format(len(CAMERA_LIST), CONFIG_FILE))
print("List of Cameras : ", CAMERA_LIST)

gpus = physical_devices_list_to_dict(tf.config.list_physical_devices('GPU'))
cpus = physical_devices_list_to_dict(tf.config.list_physical_devices('CPU'))
print("Found GPUs : ", gpus)
print("Found CPUs : ", cpus)
logical_devices_dict = get_device_to_model_map(gpu_dict=gpus, cpu_dict=cpus, model_list=CAMERA_LIST, memory_per_model=MEM_PER_MODEL)
for key in logical_devices_dict.keys():
    print('Camera {} is mapped to {}'.format(key, logical_devices_dict[key]))
weight_file_path_dict = get_weight_file_path_dict(config_dict=CONFIG_DICT, data_dir=DATA_DIR)
model_dict = get_and_load_models(weight_file_path_dict=weight_file_path_dict, logical_devices_dict=logical_devices_dict)
data_generator_dict = get_datagenrator_dict(config_dict=CONFIG_DICT, data_dir=DATA_DIR)

def insert_inference():
    all_output = []
    print("Hello")
    for key in data_generator_dict.keys():
        try:
            new_batch = next(iter(data_generator_dict[key].get_dataset()))
            ai_manager_config = get_AI_manager_details(CONFIG_DICT)
        except Exception as e:
            return jsonify({"status": "complete", "camera_ID":key})
        orientation = data_generator_dict[key].orientation
        output_dict = run_inference_on_one_image(image_batch=new_batch, base_model=model_dict[key], threshold=CONFIG_DICT[key]['Thresold'], num_ref_images=data_generator_dict[key].total_ref_sample, camera_ID=key, orientation=orientation, ip_shape=data_generator_dict[key].input_shape)
        all_output.append(output_dict)
        response_object = {"views": all_output, "label": output_dict["batch_result"], "status": "active", "ai_manager_config": ai_manager_config}
        next_inference(output_dict, ai_manager_config)

    return response_object
    
def get_all_inference():
    return select_all_inference()
    
def get_calendar():
    start_date = request.args.get('from', default = '2020-01-01 12:01:01', type = str)
    end_date = request.args.get('to', default = '2021-01-01 12:01:01', type = str)
    return calendar(start_date, end_date)

'''