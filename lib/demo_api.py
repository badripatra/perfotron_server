""" === DEPLOY REST API For Perf Dashboard Demo ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "bpatra@netapp.com"
__status__ = "Testing"
 === DEPLOY REST API For Perf Dashboard Demo =="""

import sys
from flask import Flask
from flask import request

FLASK_APP = Flask(__name__)
PORT = int("9003")


@FLASK_APP.route('/demo_api_get')
def demo_rest_api():
    """ This function is responsible to deploy a GET API """
    return "demo rest api"


@FLASK_APP.route('/demo_api_post', methods=['POST'])
def api_message():
    """ This function is responsible to deploy a POST API """
    return request.data


sys.exit(FLASK_APP.run(host='0.0.0.0', port=PORT, processes=2, threaded=False))
