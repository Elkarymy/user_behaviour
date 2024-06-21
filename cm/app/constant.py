CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'

CM_REGISTER_Q = 'rpc_queue_CM_register'  # Do not change this value

CM_NAME = 'CM - Behavioural interventions'
RPC_CM_ALIVE = 'rpc_queue_CM_ALIVE'  # Do not change this value
RPC_Q = 'rpc_queue_CM_compute'  # Do not change this value
CM_ID = 27  # CM_ID is defined by the energy research center of Martigny (CREM)
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80

# TODO ********************setup this URL depending on which version you are running***************************

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER

# TODO ********************setup this URL depending on which version you are running***************************
TRANFER_PROTOCOLE = 'http://'
# =============================================================================
#
# =============================================================================


INPUTS_CALCULATION_MODULE = [
    {
        'cm_id': CM_ID,
        'input_max': '',
        'input_min': '',
        'input_name': 'Country',
        'input_parameter_name': 'nuts0_code',
        'input_type': 'select',
        'input_unit': '',
        'input_value': ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","EL","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE","UK","ALL"]
    },
    {
        'cm_id': CM_ID,
        'input_max': '',
        'input_min': '',
        'input_name': 'Intervention type',
        'input_parameter_name': 'intervention_type',
        'input_type': 'select',
        'input_unit': '',
        'input_value': ['All', 'Monetary incentives', 'Providing feedback and information',
                        'Nudging occupants', 'Policy']
    },
    {
       'cm_id': CM_ID,
        'input_max': '',
        'input_min': '',
        'input_name': 'Building type',
        'input_parameter_name': 'building_type',
        'input_type': 'select',
        'input_unit': '',
        'input_value': ['All', 'Residential', 'Non-residential']
    }

]


# Define the SIGNATURE dictionary
SIGNATURE = {
    "category": "Demand",
    "cm_name": CM_NAME,
    "wiki_url": "",
    "layers_needed": [],
    #not sure this will remain here
    "type_layer_needed": [{"type": "nuts_id_number", "description": "A default layer is used here."}],
    "type_vectors_needed": [],
    "cm_url": "Do not add something",
    "cm_description":
    "This calculation module allows the user"\
    "to access country specific summer comfort requirements and expectations"\
    "and filter behavioural interventions that help "\
    "reduce SC demand.",
    "cm_id": CM_ID,
    "inputs_calculation_module": INPUTS_CALCULATION_MODULE,
    "authorized_scale": ["NUTS 0"]
}
