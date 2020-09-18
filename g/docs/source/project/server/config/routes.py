ROUTES = {
    'v1': [
        # AUTH
        {
            'summary': 'User login',
            'rule': '/auth/login',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'login',
        },
        {
            'summary': 'User logout',
            'rule': '/auth/logout',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'logout'
        },
        {
            'summary': 'Send confirmation by email',
            'rule': '/auth/resend-confirmation',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'resend_confirmation',
        },
        {
            'summary': 'Email Confirmation for registered user',
            'rule': '/auth/confirm-email',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'confirm_email',
        },
        {
            'summary': 'Reset password once forgotten',
            'rule': '/auth/confirm-reset-password',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'confirmed_reset_password',
        },
        {
            'summary': 'Change password once reset request is sent',
            'rule': '/user/change-password',
            'method': 'POST',
            'endpoint': 'auth',
            'function': 'change_password'
        },
        # USERS
        {
            'summary': 'Get current user',
            'rule': '/user/me',
            'method': 'GET',
            'endpoint': 'user',
            'function': 'get_current',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Post the user',
            'rule': '/user/get-user',
            'method': 'POST',
            'endpoint': 'user',
            'function': 'get_user',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get list of users',
            'rule': '/user/get-list',
            'method': 'GET',
            'endpoint': 'user',
            'function': 'get_list',
            'opts': {
                'use_pagination': True,
                'auth_required': True,
                'auth_roles': ['ADMIN']
            }
        },
        {
            'summary': 'Register the user',
            'rule': '/user/register',
            'method': 'POST',
            'endpoint': 'user',
            'function': 'register',
        },
        {
            'summary': 'Reset password for the user',
            'rule': '/user/reset-password',
            'method': 'POST',
            'endpoint': 'user',
            'function': 'reset',
        },
        {
            'summary': 'Patch current user',
            'rule': '/user/me',
            'method': 'PATCH',
            'endpoint': 'user',
            'function': 'patch_current',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Patch user with user ID',
            'rule': '/user/<int:user_id>',
            'method': 'PATCH',
            'endpoint': 'user',
            'function': 'patch_user',
            'opts': {
                'auth_required': True,
                'auth_roles': ['ADMIN']
            }
        },
        {
            'summary': 'Delete user with user ID',
            'rule': '/user/<int:user_id>',
            'method': 'DELETE',
            'endpoint': 'user',
            'function': 'delete_user',
            'opts': {
                'auth_required': True,
                'auth_roles': ['ADMIN']
            }
        },
        {
            'summary': 'Update username of user',
            'rule': '/user/username/update',
            'method': 'POST',
            'endpoint': 'user',
            'function': 'update_current',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get roles of user',
            'rule': '/user/roles',
            'method': 'GET',
            'endpoint': 'user',
            'function': 'get_role',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        # AGENTS
        {
            'summary': 'Save AI agent',
            'rule': '/ai-agent/save-agent',
            'method': 'POST',
            'endpoint': 'agent',
            'function': 'save_agent',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Modify AI agent with agent ID',
            "rule": "/ai-agent/<int:agent_id>",
            "method": "PATCH",
            "endpoint": "agent",
            "function": "modify_agent",
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get AI agent',
            'rule': '/ai-agent/get-agent',
            'method': 'GET',
            'endpoint': 'agent',
            'function': 'get_agent',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Delete AI agent as per agent ID',
            'rule': '/ai-agent/<int:agent_id>',
            'method': 'DELETE',
            'endpoint': 'agent',
            'function': 'delete_agent',
            'opts': {
                'auth_required': True
            }
        },
        # CAMERA
        {
            'summary': 'Save camera preset',
            'rule': '/camera/save-preset',
            'method': 'POST',
            'endpoint': 'camera',
            'function': 'save_preset',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get all camera preset',
            'rule': '/camera/get-all',
            'method': 'GET',
            'endpoint': 'camera',
            'function': 'select_all_preset',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        # MODEL
        {
            'summary': 'Get all models',
            'rule': '/models/get-all',
            'method': 'GET',
            'endpoint': 'models',
            'function': 'get_models',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Insert models',
            'rule': '/models/save-models',
            'method': 'POST',
            'endpoint': 'models',
            'function': 'insert_model',
            'opts': {
                'use_pagination': False,
                'auth_required': True
            }
        },
        {
            'summary': 'Get image attributes',
            'rule': '/image/get-all-attributes',
            'method': 'GET',
            'endpoint': 'image',
            'function': 'get_all_attributes',
            'opts': {
                'use_pagination': True,
                'auth_required': False
            }
        },
        {
            'summary': 'Get list of images',
            'rule': '/image/get-image-list',
            'method': 'GET',
            'endpoint': 'image',
            'function': 'get_image_list',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Change image attributes',
            'rule': '/image/change-all-attributes',
            'method': 'POST',
            'endpoint': 'image',
            'function': 'change_all_attributes',
            'opts': {
                'use_pagination': False,
                'auth_required': False
            }
        },
        {
            'summary': 'Change image',
            'rule': '/image/change-image',
            'method': 'POST',
            'endpoint': 'image',
            'function': 'change_image',
            'opts': {
                'use_pagination': False,
                'auth_required': True
            }
        },
        # DATASET
        {
            'summary': 'Get dataset list',
            'rule': '/dataset',
            'method': 'GET',
            'endpoint': 'dataset',
            'function': 'get_list',
            'opts': {
                'use_pagination': True,
                'auth_required': False
            }
        },
        {
            'summary': 'Create dataset',
            'rule': '/dataset',
            'method': 'PUT',
            'endpoint': 'dataset',
            'function': 'create',
            'opts': {
                'auth_required': False
            }
        },
        {
            'summary': 'Get dataset with given ID',
            'rule': '/dataset/<int:dataset_id>',
            'method': 'GET',
            'endpoint': 'dataset',
            'function': 'get',
            'opts': {
                'use_pagination': True,
                'auth_required': False
            }
        },
        {
            'summary': 'Update dataset with given ID',
            "rule": "/dataset/<int:dataset_id>",
            "method": "PATCH",
            "endpoint": "dataset",
            "function": "update",
            'opts': {
                'auth_required': False
            }
        },
        {
            'summary': 'Delete dataset with given ID',
            'rule': '/dataset/<int:dataset_id>',
            'method': 'DELETE',
            'endpoint': 'dataset',
            'function': 'delete',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get images in dataset with given ID',
            'rule': '/dataset/<int:dataset_id>/images',
            'method': 'GET',
            'endpoint': 'dataset',
            'function': 'get_images',
            'opts': {
                'use_pagination': True,
                'auth_required': False
            }
        },
        {
            'summary': 'Add images in dataset with given ID',
            'rule': '/dataset/<int:dataset_id>/images',
            'method': 'PUT',
            'endpoint': 'dataset',
            'function': 'add_images',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get images with filename in dataset with given ID',
            'rule': '/dataset/<string:dataset_id>/images/<string:filename>',
            'method': 'GET',
            'endpoint': 'dataset',
            'function': 'get_image',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Delete images in dataset with given ID',
            'rule': '/dataset/<int:dataset_id>/images/<int:image_id>',
            'method': 'DELETE',
            'endpoint': 'dataset',
            'function': 'delete_image',
            'opts': {
                'auth_required': True
            }
        },
        # ANNOTATION
        {
            'summary': 'Get annotation list',
            'rule': '/annotation',
            'method': 'GET',
            'endpoint': 'annotation',
            'function': 'get_list',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Create annotation',
            'rule': '/annotation',
            'method': 'PUT',
            'endpoint': 'annotation',
            'function': 'create',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Update annotation with given ID',
            "rule": "/annotation/<int:annotation_id>",
            "method": "PATCH",
            "endpoint": "annotation",
            "function": "update",
            'opts': {
                'auth_required': False
            }
        },
        {
            'summary': 'Get annotation with given ID',
            'rule': '/annotation/<int:annotation_id>',
            'method': 'GET',
            'endpoint': 'annotation',
            'function': 'get',
            'opts': {
                'auth_required': False
            }
        },
        {
            'summary': 'Delete annotation with given ID',
            'rule': '/annotation/<int:annotation_id>',
            'method': 'DELETE',
            'endpoint': 'annotation',
            'function': 'delete',
            'opts': {
                'auth_required': True
            }
        },
        # ATTRIBUTE
        {
            'summary': 'Get attribute list',
            'rule': '/attribute',
            'method': 'GET',
            'endpoint': 'attribute',
            'function': 'get_list',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Create attribute',
            'rule': '/attribute',
            'method': 'PUT',
            'endpoint': 'attribute',
            'function': 'create',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get attribute with given ID',
            "rule": "/attribute/<int:attribute_id>",
            "method": "GET",
            "endpoint": "attribute",
            "function": "get",
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Update attribute with given ID',
            "rule": "/attribute/<int:attribute_id>",
            "method": "PATCH",
            "endpoint": "attribute",
            "function": "update",
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Delete attribute with given ID',
            'rule': '/attribute/<int:attribute_id>',
            'method': 'DELETE',
            'endpoint': 'attribute',
            'function': 'delete',
            'opts': {
                'auth_required': True
            }
        },
        # CATEGORY
        {
            'summary': 'Get category list',
            'rule': '/category',
            'method': 'GET',
            'endpoint': 'category',
            'function': 'get_list',
            'opts': {
                'use_pagination': True,
                'auth_required': True
            }
        },
        {
            'summary': 'Create category',
            'rule': '/category',
            'method': 'PUT',
            'endpoint': 'category',
            'function': 'create',
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Get category with given ID',
            "rule": "/category/<int:category_id>",
            "method": "GET",
            "endpoint": "category",
            "function": "get",
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Update category with given ID',
            "rule": "/category/<int:category_id>",
            "method": "PATCH",
            "endpoint": "category",
            "function": "update",
            'opts': {
                'auth_required': True
            }
        },
        {
            'summary': 'Delete category with given ID',
            'rule': '/category/<int:category_id>',
            'method': 'DELETE',
            'endpoint': 'category',
            'function': 'delete',
            'opts': {
                'auth_required': True
            }
        },
        # INFERENCE
        {
            'summary': 'Get Inference',
            'rule': '/inference',
            'method': 'GET',
            'endpoint': 'inference',
            'function': 'inference',
            'opts': {
                'use_pagination': False,
                'auth_required': False
            }
        },
    ]
}
