""" === Setting a System Monitor for Perf Dashboard ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
=== Setting a System Monitor for Perf Dashboard  =="""

import subprocess
import ConfigParser
import os
import socket
from time import time
from time import sleep
from influxdb import InfluxDBClient

SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))  # Get directory location for script
os.chdir(SCRIPTDIR)  # Switch to Script Directory. Setting for the cron to run
os.environ["TERM"] = "dumb"
HOSTNAME = socket.gethostname()


# This method will take the command as a string parameter and fire the shell and return the output
def get_command_output():
    """ This function is responsible for running a command on Shell & return output"""
    process = subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()[0]
    return output


def push_data_influx(measurement_name, counter_name, counter_value, current_time):
    """ This function is responsible for push data to influx"""

    json_body = [{"measurement": measurement_name, "time": current_time * 1000,
                  "tags": {"server": HOSTNAME}, "fields": {"hostname": HOSTNAME,
                                                           "counter_name": counter_name,
                                                           "counter_value": float(counter_value)}}]

    CLIENT.write_points(json_body, time_precision='ms')


CONFIG = ConfigParser.ConfigParser()
CONFIG.read('server_stats.ini')

CLIENT = InfluxDBClient(host='localhost', port=8086, username='lnp_automation',password='lnp_automation')
CLIENT.switch_database('jmeter')


while True:
    sleep(60)
    for command_name in CONFIG.options('Commands'):
        sleep(1)
        COMMAND = CONFIG.get('Commands', command_name)
        COMMAND_OUTPUT = str(get_command_output()).strip()
        CURRENT_TIME = int(time())
        push_data_influx("server_stats", command_name, COMMAND_OUTPUT, CURRENT_TIME)
