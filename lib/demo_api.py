""" === DEPLOY REST API For Perf Dashboard Demo ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "bpatra@netapp.com"
__status__ = "Testing"
 === DEPLOY REST API For Perf Dashboard Demo =="""

import sys
from flask import Flask, render_template
from flask import request

FLASK_APP = Flask(__name__)
PORT = int("9003")
ALLOWED_EXTENSIONS = {'jmx'}


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
                return content
            else:
                return render_template('file_extension_not_allowed.html')

        else:
            return render_template('empty_file.html')

    return render_template('upload.html')


sys.exit(FLASK_APP.run(host='0.0.0.0', port=PORT, processes=2, threaded=False))
