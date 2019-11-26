""" === DEPLOY REST API For Perf Dashboard Demo ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "bpatra@netapp.com"
__status__ = "Testing"
 === DEPLOY REST API For Perf Dashboard Demo =="""

import os
import sys
from flask import Flask, render_template, send_file
from flask import request
from xml.etree import ElementTree as ET
import subprocess
import time

FLASK_APP = Flask(__name__)
PORT = int("9003")
ALLOWED_EXTENSIONS = {'jmx'}
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_jmxchecker_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        cmd_value = str(cmd.stdout.readlines()).strip()  # Read command output
        sys.stdout.flush()
    except IndexError:
        cmd_value = ""

    return cmd_value


def get_command_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        cmd_value = str(cmd.stdout.readlines()[0]).strip()  # Read command output
        sys.stdout.flush()
    except IndexError:
        cmd_value = ""

    return cmd_value


def add_backend_listner(jmx_string):
    """ This function is responsible for adding back end listener to a existing jmx"""

    with open('user_script.jmx', "w") as backend_listner:
        backend_listner.write(jmx_string)

    backend_listener = ET.parse("backend_listner.jmx")

    base_script = ET.parse('user_script.jmx')
    existing_struct = base_script.find("./hashTree/hashTree")
    new_condition = backend_listener.getroot()
    existing_struct.append(new_condition)

    epoch_time = str(int(time.time()))

    file_name = 'user_script_'+epoch_time

    with open(file_name, "w") as user_jmx:
        user_jmx.write(ET.tostring(base_script.getroot()))

    return file_name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@FLASK_APP.route('/demo_api_get')
def demo_rest_api():
    """ This function is responsible to deploy a GET API """
    return "demo rest api"


@FLASK_APP.route('/demo_api_post', methods=['POST'])
def api_message():
    """ This function is responsible to deploy a POST API """
    return request.data


@FLASK_APP.route('/convert_jmx', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        file = request.files['file']

        if file:
            if allowed_file(file.filename):
                content = file.read()
                modified_jmx = add_backend_listner(content)
                return send_file(modified_jmx, attachment_filename=modified_jmx)
                
            else:
                return render_template('file_extension_not_allowed.html')

        else:
            return render_template('empty_file.html')

    return render_template('upload.html')


sys.exit(FLASK_APP.run(host='0.0.0.0', port=PORT, processes=2, threaded=False))
