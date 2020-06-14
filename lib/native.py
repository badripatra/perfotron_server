""" ===Main Scripts to install influx, grafana set up env==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
===Main Scripts to install influx, grafana, set up env=="""

import datetime
import os
from time import sleep
import subprocess
import sys
import ConfigParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_OBJECT = ConfigParser.ConfigParser()
CONFIG_OBJECT.optionxform = str
CONFIG_OBJECT.read(os.path.join(CURRENT_DIR,"config.cnf"))

# ------------------------------Functions---------------------------------------------------


def timer_logger(start_time, end_time, component, acitivity):
    """ This function is used for logging """
    log_line = [str(start_time), str(end_time), str(end_time - start_time), component, acitivity]
    timer_log_file_name = os.path.join(CURRENT_DIR, "installation_timer.log")
    os.system("echo " + ','.join(log_line) + " >> " + timer_log_file_name)


def detailed_logger(current_time, activity, log_file_name):
    """ This function is responsible for logging """
    os.system('echo "---------' + activity + '-----------------"' + ' >> '+log_file_name)
    os.system("echo " + current_time + " >> " + log_file_name)


def get_ip(cloud_vendor):
    """ This function is responsible for getting ip address cloud / on-promise systm  """
    if cloud_vendor != "NA":
        ip_address = get_command_output("curl -s ifconfig.me")
    else:
        ip_address = get_command_output('hostname -I|cut -d " " -f1')


    return ip_address


def get_command_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_value = str(cmd.stdout.readlines()[0]).strip()  # Read command output
    sys.stdout.flush()
    return cmd_value


def invoke_rest_api(project_dir):
    """ This function is responsible for invoke a test api for demo"""
    file_name = os.path.join(project_dir, "invoke_restapis.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Invoke Demo REST API", log_file_name)

    command = file_name + " >> " + file_name.replace(".sh", ".log") + " 2>&1"
    os.system(command)
    #print "Command Triggered : " + command


def invoke_stats_collector(project_dir):
    """ This function is responsible for invoke system stats collector"""
    file_name = os.path.join(project_dir, "invoke_serverstats.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Invoke Stats Collector", log_file_name)

    command = file_name + " >> " + file_name.replace(".sh", ".log") + " 2>&1"
    os.system(command)
    #print "Command Triggered : " + command


def enable_ports(project_dir):
    """ This function is responsible for enabling ports on system"""
    print "Step 1. : Enabling Grafana Port (3000), Influx Port (8086), Demo API (9003)"
    file_name = os.path.join(project_dir, "enable_ports.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Enabling Ports", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "PORTS", "Enabling Ports 3000 8086 9003")

    #print "Command Triggered : " + command
    print "\n"


def influx_setup(project_dir):
    """ This function is responsible for installing influx"""
    print "Step 2. : Setting up Influx DB."
    file_name = os.path.join(project_dir, "influx_setup.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Influx Set Up", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "INFLUX", "Installing INFLUX")

    #print "Command Triggered : " + command
    print "\n"


def grafana_setup(project_dir):
    """ This function is responsible for installing grafana server"""
    print "Step 3. : Setting up Grafana"
    file_name = os.path.join(project_dir, "grafana_setup.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Grafana Set Up", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "GRAFANA", "Installing GRAFANA")

    #print "Command Triggered : " + command
    print "\n"


def grafana_add_datasource(project_dir):
    """ This function is responsible for adding datasource for grafana"""
    print "Step 4. : Adding DataSource(Influx DB) for Grafana"
    file_name = os.path.join(project_dir, "add_grafana_datasource.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Add Grafana DataSource", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "GRAFANA", "Add Datasource for GRAFANA")

    #print "Command Triggered : " + command
    print "\n"


def grafana_add_dashboard(project_dir):
    """ This function is responsible for adding sample Perfortron dashboard"""
    print "Step 5. : Setting up Sample Perfotron Dashboard"
    file_name = os.path.join(project_dir, "add_grafana_dashboard.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Add Perfotron Dashboard", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "GRAFANA", "Add Perfotron Dashboard")

    #print "Command Triggered : " + command
    print "\n"


def deploy_demo_api(project_dir):
    """ This function is responsible for adding Perfotron dashboard"""
    print "Step 6. : Deploying a REST Application on Hosting Server for Live Demo"

    start_time = datetime.datetime.now()
    invoke_rest_api(project_dir)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "Test API", "Deploying Test API")

    print "\n"


def deploy_stats_collector(project_dir):
    """ This function is responsible for triggering system stats collector"""
    print "Step 7. : Setting up periodic system stats (cpu,memory,disk) collections"

    start_time = datetime.datetime.now()
    invoke_stats_collector(project_dir)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "System Stats", "Collecting System Stats")

    print "\n"

def setup(root_project_directory, input_map):
    """ Main Function"""

    cloud_vendor = input_map["cloud_vendor"]

    ip_address = get_ip(cloud_vendor)

    start_time = datetime.datetime.now()
    print "-----------------------Progress---------------------------------------"

    #dependency_resolution(root_project_directory)
    enable_ports(root_project_directory)
    influx_setup(root_project_directory)
    grafana_setup(root_project_directory)
    grafana_add_datasource(root_project_directory)
    grafana_add_dashboard(root_project_directory)
    deploy_demo_api(root_project_directory)
    deploy_stats_collector(root_project_directory)

    print "-------------------Progress------------------------------------------"

    end_time = datetime.datetime.now()
    print "SET-UP Start Time :" + str(start_time)
    print "SET-UP End Time : " + str(end_time)
    print "Total Time Taken : " + str(end_time - start_time)
    print "\n"

    convertor_url = CONFIG_OBJECT.get('API', 'CONVERTER_URL')
    convertor_url = convertor_url.replace("ip_address", ip_address)

    jmx_generator_url = CONFIG_OBJECT.get('API', 'GENERATE_JMX_URL')
    jmx_generator_url = jmx_generator_url.replace("ip_address", ip_address)

    home_url = CONFIG_OBJECT.get('API', 'HOME_PAGE')
    home_url = home_url.replace("ip_address", ip_address)

    perf_dashboard_url = CONFIG_OBJECT.get('DASHBOARD', 'URL')
    perf_dashboard_url = perf_dashboard_url.replace("ip_address", ip_address)

    token = get_command_output("cat token.txt")


    print "-------------------References------------------------------------------"
    print "PerfoTron Dashboard                : " + perf_dashboard_url + " (credentials : admin/admin)"
    print "For all documentation              : " + home_url
    print "Users familiar with Jmeter, to get started use 'PerfoTron JMX Convertor'."
    print "PerfoTron JMX Convertor            : " + convertor_url + ". Token : " + token
    print "                                   OR                                   "
    print "Users not familiar with Jmeter, to get started use 'get_jmxchecker_output'."
    print "PerfoTron JMX Generator            : " + jmx_generator_url
    print "-------------------References------------------------------------------"
# ---------------------------Functions----------------------------------------------------


if __name__ == "__main__":

    os.chdir(CURRENT_DIR)

    INPUT_MAP = {}
    for arg in sys.argv:
        if ":" in arg:
            Key = arg.split(":")[0]
            Value = arg.split(":")[1]
            INPUT_MAP[Key] = Value
    setup(CURRENT_DIR, INPUT_MAP)
