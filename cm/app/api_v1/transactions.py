
from flask import request, abort, jsonify ,url_for, g,flash
from . import api
from .. import SIGNATURE,CM_NAME
import json
import requests
import logging
import os
from flask import send_from_directory
from  app import helper
from app import constant

from app.api_v1 import errors
import socket
from . import calculation_module
from app import CalculationModuleRpcClient



LOG_FORMAT = (
    '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
    '-35s %(lineno) -5d: %(message)s'
)
LOGGER = logging.getLogger(__name__)


UPLOAD_DIRECTORY = '/var/tmp'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    os.chmod(UPLOAD_DIRECTORY, 0o777)


@api.route('/files/<string:filename>', methods=['GET'])
def get(filename):
    # get file stored in the api directory
    return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)


@api.route('/register/', methods=['POST'])
def register():
    # Register the Calculation module (CM) to the main web services (MWS).
    # The CM will send its SIGNATURE to the main web service. CM SIGNATURE
    # contains elements to identify the CM and how to handle it and the list
    # of inputs it needs on the user interface. CM SIGNATURE can be found in
    # app/constants.py file, and this file must be changed manually. Also,
    # constants.py must contain a CM_ID that is a unique number that has to be
    # defined by the CREM (Centre de Recherches Energetiques et Municipales de
    # Martigny).
    print('CM will begin register ')
    ip = socket.gethostbyname(socket.gethostname())
    base_url = 'http://' + str(ip) + ':' + str(constant.PORT) + '/'
    signature_final = SIGNATURE

    calculation_module_rpc = CalculationModuleRpcClient()

    signature_final["cm_url"] = base_url
    payload = json.dumps(signature_final)
    response = calculation_module_rpc.call(payload)

    return response


def savefile(filename, url):
    LOGGER.info('CM is Computing and will download files with url: %s', url)
    r = None
    path = None
    try:
        r = requests.get(url, stream=True)
    except:
        LOGGER.error('API unable to download tif files')

    LOGGER.info('Image saved: %d', r.status_code)
    if r.status_code == 200:
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        LOGGER.error('API unable to download tif files')

    return path


@api.route('/compute/', methods=['POST'])
def compute():
    # Compute the Calculation module (CM) from the main web services (MWS).
    # The main web service is sending.
    print('CM will Compute ')

    data = request.get_json()
    # Inputs layers and parameters
    inputs_raster_selection = helper.validateJSON(data["inputs_raster_selection"])

    inputs_parameter_selection = helper.validateJSON(data["inputs_parameter_selection"])


    output_directory = UPLOAD_DIRECTORY

    # Call the calculation module function
    result = calculation_module.calculation(output_directory, inputs_parameter_selection)

    response = {
        'result': result
    }

    # Convert response dict to json
    response = json.dumps(response)
    return response
