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
import generate_jmx

FLASK_APP = Flask(__name__)
PORT = int("9003")
ALLOWED_EXTENSIONS = {'jmx'}
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

with open("token.txt", "r") as token_file:
    token = str(token_file.read().strip())

def get_jmxchecker_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        cmd_value = str(cmd.stdout.readlines()).strip()  # Read command output
        sys.stdout.flush()
    except IndexError:
        cmd_value = ""

    return cmd_value


def add_backend_listner(jmx_string, application_name):
    """ This function is responsible for adding back end listener to a existing jmx"""

    epoch_time = str(int(time.time()))

    user_jmx_name = 'original_user_'+epoch_time+'.jmx'

    with open(user_jmx_name, "w") as user_jmx:
        user_jmx.write(jmx_string)

    jmx_validity = get_jmxchecker_output(
        "~/installation_launchpad/apache-jmeter-5.1.1/bin/TestPlanCheck.sh --jmx "+ user_jmx_name)

    if "JMX is fine" not in jmx_validity:

        print "The Jmeter Script is not valid. Please correct it and Retry"
        return "Invalid JMX"

    else:
        os.system("sed -i -e 's/\[app\]/" + application_name + "/g' backend_listner.jmx")
        backend_listener = ET.parse("backend_listner.jmx")

        base_script = ET.parse(user_jmx_name)
        existing_struct = base_script.find("./hashTree/hashTree")
        new_condition = backend_listener.getroot()
        existing_struct.append(new_condition)

        file_name = 'converted_user_'+epoch_time+'.jmx'

        with open(file_name, "w") as user_jmx:
            user_jmx.write(ET.tostring(base_script.getroot()))

        return file_name


def allowed_file(filename):
    """ This function is responsible checking if file name contains required extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@FLASK_APP.route('/')
def home():
    """ This function is responsible to deploy Home Page"""
    return render_template('home.html')


@FLASK_APP.route('/system_requirement')
def system_requirement():
    """ This function is responsible to deploy Home Page"""
    return render_template('system_requirement.html')


@FLASK_APP.route('/install_onprem')
def install_onprem():
    """ This function is responsible to deploy Home Page"""
    return render_template('install_onprem.html')


@FLASK_APP.route('/install_gcp')
def install_gcp():
    """ This function is responsible to deploy Home Page"""
    return render_template('install_gcp.html')


@FLASK_APP.route('/install_aws')
def install_aws():
    """ This function is responsible to deploy Home Page"""
    return render_template('install_aws.html')


@FLASK_APP.route('/install_azure')
def install_azure():
    """ This function is responsible to deploy Home Page"""
    return render_template('install_azure.html')


@FLASK_APP.route('/explain_usage')
def explain_usage():
    """ This function is responsible to deploy Home Page"""
    return render_template('explain_usage.html')


@FLASK_APP.route('/demo_api_get')
def demo_api_get():
    """ This function is responsible to deploy a GET API Route"""
    return "demo rest api"


@FLASK_APP.route('/demo_api_post', methods=['POST'])
def demo_api_post():
    """ This function is responsible to deploy a POST API Route"""
    return request.data

@FLASK_APP.route('/sample_jmx')
def sample_jmx_download ():
    path = "/jmx/sample_jmeter_script.jmx"
    return send_file(path, as_attachment=True)

@FLASK_APP.route('/sample_csv_download')
def sample_csv_download ():
    path = "sample_scenario_file.csv"
    return send_file(path, as_attachment=True)


@FLASK_APP.route('/download_jmx/<filename>')
def download_jmx(filename):
    return send_file(filename, mimetype='text/jmx', as_attachment=True)

@FLASK_APP.route('/convert_csv', methods=['GET', 'POST'])
def convert_csv():
    """ This function is responsible to deploy a Convert CSV Route """

    if request.method == 'POST':
        file_object = request.files['file']
        content = file_object.read()
        epoch_time = str(int(time.time()))

        input_file_name = file_object.filename
        fileName, fileExtension = os.path.splitext(input_file_name)
        user_csv_file = fileName+"_"+epoch_time+fileExtension
        converted_jmx_file = user_csv_file.replace(".csv", ".jmx")

        create_jmx_obj = generate_jmx.create_jmx_scenario(content, user_csv_file, converted_jmx_file)

        create_jmx_obj.form_jmx_file()
        return send_file(converted_jmx_file, mimetype='text/jmx', as_attachment=True)

    return render_template('generate_jmeter_script.html')


@FLASK_APP.route('/convert_jmx', methods=['GET', 'POST'])
def convert_jmx():
    """ This function is responsible to deploy a Convert JMX Route """

    if request.method == 'POST':

        file_object = request.files['file']
        user_input_token = request.form['token']
        application_name = request.form['AUT']

        if allowed_file(file_object.filename):

            content = file_object.read()
            modified_jmx_file = add_backend_listner(content, application_name)

            if modified_jmx_file == "Invalid JMX":
                return render_template('Invalid_jmx.html')

            else:

                if user_input_token == token:
                    return render_template('File_Uploaded.html', filename=modified_jmx_file)
                else:
                    return render_template('Invalid_token.html')

        else:
            return render_template('file_extension_not_allowed.html')


    return render_template('convert.html')


sys.exit(FLASK_APP.run(host='0.0.0.0', port=PORT, processes=2, threaded=False))
