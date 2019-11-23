""" ===Main Scripts to install influx, grafana, jenkins and set up env==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
===Main Scripts to install influx, grafana, jenkins and set up env=="""

import datetime
import os
from time import sleep
import socket
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
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

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
    print "Command Triggered : " + command


def invoke_stats_collector(project_dir):
    """ This function is responsible for invoke system stats collector"""
    file_name = os.path.join(project_dir, "invoke_serverstats.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Invoke Stats Collector", log_file_name)

    command = file_name + " >> " + file_name.replace(".sh", ".log") + " 2>&1"
    os.system(command)
    print "Command Triggered : " + command


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

    print "Command Triggered : " + command
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

    print "Command Triggered : " + command
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

    print "Command Triggered : " + command
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

    print "Command Triggered : " + command
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

    print "Command Triggered : " + command
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


def enable_jenkins_port(project_dir):
    """ This function is responsible for enable jenkins port 8080"""
    print "Step 8. : Live Demo  : Jenkins - > Jmeter -> Perfotron Dashboard "
    print "\n"
    print "          Enabling Jenkins Port :- "
    file_name = os.path.join(project_dir, "enable_jenkins_ports.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Enable Jenkins Ports", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "JENKINS", "EnablingF Jenkins Port 8080")

    print "          Command Triggered : " + command
    print "\n"


def jenkins_installation(project_dir):
    """ This function is responsible for jenkins installation  """
    print "          Jenkins Installation :- "
    file_name = os.path.join(project_dir, "jenkins_installation.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Jenkins Installation", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "JENKINS", "Installing JENKINS")

    print "          Command Triggered : " + command
    print "\n"


def setup_adminuser_jenkins(project_dir):
    """ This function is responsible for set up admin user for jenkins"""
    sleep(90)
    print "          Unlock Jenkins :- "
    file_name = os.path.join(project_dir, "unlock_jenkins.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Unlock Jenkins", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "JENKINS", "Set-up Admin User")

    print "          Command Triggered : " + command
    print "\n"


def jenkins_job_setup(project_dir):
    """ This function is responsible for set up demo jenkins job"""
    print "          Jenkins Job Set up :- "
    file_name = os.path.join(project_dir, "jenkins_job_setup.sh")
    log_file_name = os.path.join(project_dir, "Installation_details.log")

    current_time = str(datetime.datetime.now())
    detailed_logger(current_time, "Demo Job Set up", log_file_name)

    command = file_name + " >> " + log_file_name + " 2>&1"

    start_time = datetime.datetime.now()
    os.system(command)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "JENKINS", "Demo job set-up")

    print "          Command Triggered : " + command
    print "\n"


def demo_run_jenkins(jenkins_ip):
    """ This function is responsible for triggering demo jenkins job for Perfotron dashboard"""
    sleep(90)
    print "          Triggering Jenkins Job for ingesting load on demo api"
    jenkins_job_trigger_url = CONFIG_OBJECT.get('JENKINS', 'JOB_TRIGGER_URL')
    jenkins_job_trigger_url = jenkins_job_trigger_url.replace("jenkins_ip", jenkins_ip)

    start_time = datetime.datetime.now()
    os.system(jenkins_job_trigger_url)
    end_time = datetime.datetime.now()
    timer_logger(start_time, end_time, "JENKINS", "Demo Run")

    print "\n"
    print "Please wait for 2 Minutes till the Jenkins Run gets over"

    print "INFO : "
    jenkins_job_url = CONFIG_OBJECT.get('JENKINS', 'JOB_URL')
    jenkins_job_url = jenkins_job_url.replace("jenkins_ip", jenkins_ip)
    print "Jenkins Run Details : "+jenkins_job_url


def env_details_file(project_dir):
    """ Generating env details files for reference"""

    ip_address = get_ip()

    with open(os.path.join(project_dir, "details_template.yaml"), "r") as details_file:
        details = details_file.read()

    details = details.replace("[grafana_ip]", str(ip_address))
    details = details.replace("[influx_ip]", str(ip_address))
    details = details.replace("[hosting_server_ip]", str(ip_address))
    if jenkins_installation == "true":
        details = details.replace("[jenkins_ip]", str(ip_address))

    details_file = os.path.join(project_dir, "env_details.yaml")

    with open(details_file, "w") as env_details:
        env_details.write(details)

    print "** Env details contains below info : "
    print "1. Perfrotron Dashboard URL, Credentials "
    print "2. Influx DB Host name, Port, Database, Mesaurement Name"
    print "3. Sample API (which is used for demo load test) details"


def demorun_jenkins(project_dir, ip_address):
    """ Generating env details like url, default credentials etc.."""

    enable_jenkins_port(project_dir)

    jenkins_installation(project_dir)

    setup_adminuser_jenkins(project_dir)

    jenkins_job_setup(project_dir)

    perf_dashboard_url = CONFIG_OBJECT.get('DASHBOARD', 'URL')
    perf_dashboard_url = perf_dashboard_url.replace("ip_address", ip_address)

    print "          For Live Monitoring Use Perfotron dashboard"
    print "          Perfotron dashboard URL : " + perf_dashboard_url

    demo_run_jenkins(ip_address)


def demorun_local(project_dir, ip_address):
    """ This function is responsible for Perfotron dashboard demo run from local"""
    jmeter_executable = os.path.join(project_dir, "apache-jmeter-5.1.1", "bin", "jmeter")
    jmx_file = os.path.join(project_dir, "actual_demo_jmeter_script.jmx")
    jtl_file = "jmeter_transactions.log"
    result_folder = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")

    print "For Live Monitoring Use Perfotron dashboard"
    perf_dashboard_url = CONFIG_OBJECT.get('DASHBOARD', 'URL')
    perf_dashboard_url = perf_dashboard_url.replace("ip_address", ip_address)
    print "Perfotron dashboard  URL : " + perf_dashboard_url
    print "\n"

    print "Starting Demo Load Test."
    jmeter_cmd = jmeter_executable + " -n -t " + jmx_file + " -l "+jtl_file+" -e -o "+result_folder
    print "Jmeter Command : " + jmeter_cmd
    print "\n"
    os.system(jmeter_executable + " -n -t " + jmx_file + " -l "+jtl_file+" -e -o "+result_folder)
    os.system("mv *.csv " + result_folder)
    os.system("mv jmeter_transactions.log " + result_folder)
    os.system("mv jmeter.log " + result_folder)

    print "\nTest Result is stored in  '"+result_folder+"' folder"
    print "Test Results folder contains below :"
    print "* csv files for each demo api transactions"
    print "* index.html to access Test Stats and Charts"


def setup(root_project_directory, input_map):
    """ Main Function"""

    cloud_vendor = input_map["cloud_vendor"]
    print cloud_vendor
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

    install_jekins = input_map["install_jekins"]


    if install_jekins == "true":
        demorun_jenkins(root_project_directory, ip_address)
    elif install_jekins == "false":
        demorun_local(root_project_directory, ip_address)

    print "\n"
    print "Installation details can be found in 'installation_launchpad' folder :"
    print "* All the files used for installation"
    print "* Installation Logs"
    print "* Environment details "
    print "\n"
    env_details_file(root_project_directory)

    print "-------------------Progress------------------------------------------"

    end_time = datetime.datetime.now()
    print "SET-UP Start Time :" + str(start_time)
    print "SET-UP End Time : " + str(end_time)
    print "Total Time Taken : " + str(end_time - start_time)
    print "\n"

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
