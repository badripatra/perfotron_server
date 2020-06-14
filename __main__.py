""" === Initiator ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
 === Initiator =="""

import os
import signal
import sys
import subprocess
import argparse
import datetime
from xml.etree import ElementTree as ET


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(CURRENT_DIR + '/lib'))
os.chdir(CURRENT_DIR)

HOME = os.path.expanduser("~")


def identify_onprem_or_cloud():
    """ This function is responsible to identify if a system is part of cloud provider """
    auzure = get_command_output("sudo dmidecode|grep Microsoft|wc -l")
    aws = get_command_output("sudo dmidecode|grep amazon|wc -l")
    gcp=get_command_output("sudo dmidecode|grep Google|wc -l")

    if int(auzure) > 0:
        cloud_vendor = "auzure"
    elif int(aws) > 0:
        cloud_vendor = "aws"
    elif int(gcp) > 0:
        cloud_vendor = "gcp"
    else:
        cloud_vendor = "NA"
    return cloud_vendor


def dependency_resolution():
    """ This function is responsible to install dependent packages """

    print "-----------------Resolving Dependencies-----------------------------"
    dependency_details = os.path.join(CURRENT_DIR, "os_specific_files", OS_TYPE,
                                      "install_dependency.sh")
    cmd = dependency_details + " > /dev/null 2>&1"

    print "1. pip"
    print "2. jdk (8)"
    print "3. flask (python module)"
    print "4. inquirer (python module)"
    print "5. influxdb (python module)"

    os.system(cmd)

    print "-----------------Resolving Dependencies------------------------------"


def get_ip(cloud_vendor):
    """ This function is responsible to identify clouder provider from BIOS """

    if cloud_vendor != "NA":
        ip_address = get_command_output("curl -s ifconfig.me")
    else:
        ip_address = get_command_output('hostname -I|cut -d " " -f1')

    return ip_address


def get_command_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        cmd_value = str(cmd.stdout.readlines()[0]).strip()  # Read command output
        sys.stdout.flush()
    except IndexError:
        cmd_value = ""

    return cmd_value


def check_tool_installations():
    """ This function is responsible for check if Perfotron dashboard is already installed or not"""

    '''chk_jmeter_influx = 'sudo curl -G "http://localhost:8086/query"' \
                        ' --data-urlencode "q=show databases"'
    influx = "jmeter" in get_command_output(chk_jmeter_influx)'''

    check_grafana_dashboard = 'ls -lrth /var/lib/grafana/dashboards/sample_dashboard.json'
    grafana = "sample_dashboard" in get_command_output(check_grafana_dashboard)

    #perf_dashboard_installed = bool(influx and grafana)

    perf_dashboard_installed = bool(grafana)

    return perf_dashboard_installed


def sigint_handler(signum, frame):
    """ This function is responsible for handling user abort scenarios"""
    print '\nExiting now'
    sys.exit(1)


def uninstall_perftool(package_manager):
    """ This function is responsible for uninstalling Perfotron dashboard"""

    print "Started Uninstalling the perf tool"

    print "-------------------Progress-----------------------------------------------"

    if package_manager == "rpm":

        os.system("sudo yum -y remove grafana >> ~/un-installation_details.log 2>&1")
        print "Removed Grafana Server"

        os.system("sudo yum -y remove influxdb >> ~/un-installation_details.log 2>&1")
        print "Removed Influx DB"


        os.system("sudo yum clean all >> ~/un-installation_details.log 2>&1")

    elif package_manager == "dpkg":

        os.system("sudo apt-get purge remove grafana >> ~/un-installation_details.log 2>&1")
        print "Removed Grafana Server"

        os.system("sudo apt-get purge remove influxdb >> ~/un-installation_details.log 2>&1")
        print "Removed Influx DB"


        os.system("sudo apt-get clean >> ~/un-installation_details.log 2>&1")

    print "Stopped Demo API"
    os.system("sudo kill -9 `ps -ef|grep -v grep|grep 'python demo_api.py'"
              "|awk '{print $2}'` > /dev/null 2>&1")

    print "Stopped System Data Collector"
    os.system("sudo kill -9 `ps -ef|grep -v grep|grep 'python system_monitor.py'"
              "|awk '{print $2}'` > /dev/null 2>&1")



    print "Killing existing instances of influx, grafana"
    os.system("sudo kill $(ps aux | grep -v grep| grep 'influx' | "
              "awk '{print $2}') >> ~/un-installation_details.log 2>&1")
    os.system("sudo kill $(ps aux | grep -v grep| grep 'grafana' | "
              "awk '{print $2}') >> ~/un-installation_details.log 2>&1")


    print "Removing Files and Folder related to influx, grafana"
    os.system("sudo rm -rf /var/lib/grafana >> ~/un-installation_details.log 2>&1")
    os.system("sudo rm -rf /etc/grafana/ >> ~/un-installation_details.log 2>&1")
    os.system("sudo rm -rf ~/installation_logs >> ~/un-installation_details.log 2>&1")
    os.system("sudo rm -rf ~/installation_launchpad >> ~/un-installation_details.log 2>&1")
    os.system("sudo rm -rf ~/Desktop/ >> ~/un-installation_details.log 2>&1")
    print "Deleted Corresponding Folders"

    print "--------------------Progress------------------------------------------------------------"
    print "Completed Un installing the perf tool"
    print "\n"


def native_initiator(cloud_vendor):
    """ This function is responsible for copying required files to
    installation directory and start the run"""

    os.system("mkdir -p ~/installation_launchpad")

    os.system("cp -r os_specific_files/"+OS_TYPE+"/*.* ~/installation_launchpad")

    os.system ("cp requirements.txt ~/installation_launchpad")

    os.system("cp -r grafana/*.* ~/installation_launchpad")

    os.system("mkdir -p ~/installation_launchpad/jmx")

    os.system("cp templates/jmx/*.jmx ~/installation_launchpad/jmx/")

    os.system("cp lib/demo_api.py ~/installation_launchpad")

    os.system("cp lib/generate_jmx.py ~/installation_launchpad")

    os.system("cp demo_api/invoke_restapis.sh ~/installation_launchpad")

    os.system("cp setup_details/details_template.yaml ~/installation_launchpad")

    os.system("cp server_stats/invoke_serverstats.sh ~/installation_launchpad")

    os.system("cp server_stats/server_stats.ini ~/installation_launchpad")

    os.system("cp lib/system_monitor.py ~/installation_launchpad")

    os.system("cp lib/config/config.cnf ~/installation_launchpad")

    os.system("mkdir -p ~/installation_launchpad/templates")

    os.system("mkdir -p ~/installation_launchpad/static")

    os.system("cp templates/htmls/*.html ~/installation_launchpad/templates")

    os.system("cp templates/samplers/* ~/installation_launchpad/")

    os.system("cp templates/static/*.png ~/installation_launchpad/static/")

    os.system("sed -i -e 's/\[IP\]/" + IP + "/g' ~/installation_launchpad/jmx/backend_listner.jmx")

    os.system("echo `openssl rand -hex 12` > ~/installation_launchpad/token.txt")

    os.system("sudo chown -R `id -un`:`id -gn` ~/installation_launchpad/")

    os.system("cp lib/native.py  ~/installation_launchpad")
    os.chdir(HOME)
    os.system("sudo python ~/installation_launchpad/native.py " + " cloud_vendor:" + cloud_vendor)


if __name__ == '__main__':

    signal.signal(signal.SIGINT, sigint_handler)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--uninstall", help="Uninstall Software Stack", action="store_true")

    ARGS = PARSER.parse_args()

    cloud_provider = identify_onprem_or_cloud()
    IP = get_ip(cloud_provider)
    OS_TYPE = get_command_output("python -mplatform")

    if "Ubuntu" in OS_TYPE:
        OS_TYPE = "ubuntu"
        PACKAGE_MANAGER = "dpkg"

    elif 'redhat' in OS_TYPE:
        OS_TYPE = "rhel"
        PACKAGE_MANAGER = "rpm"

    elif 'centos' in OS_TYPE:
        OS_TYPE = "centos"
        PACKAGE_MANAGER = "rpm"

    elif 'amz' in OS_TYPE:
        OS_TYPE = "amazon-linux"
        PACKAGE_MANAGER = "rpm"

    PERF_DASHBOARD = check_tool_installations()

    if not PERF_DASHBOARD:

        if ARGS.uninstall:
            print "\033[1;33;40m  '--uninstall' " \
                  "option is  only possible after Perfotron Dashboard is installed"

            print " Run 'python perfotron' command to install the Perfotron Dashboard"
            print " Exiting now\033[0;37;40m"
            sys.exit()

        else:
            with open(os.path.join(CURRENT_DIR, 'templates', 'About.txt')) as About:
                print About.read()

            dependency_resolution()  # Install all dependent modules

    import get_user_input   # Import user input lib

    if ARGS.uninstall:
        get_user_input.user_input_uninstallation()
        uninstall_perftool(PACKAGE_MANAGER)
        sys.exit()

    if not PERF_DASHBOARD:

        if cloud_provider == "gcp":
            SYSTEM_TYPE = "google_cloud"
            import google_cloud_check_n_setup
            google_cloud_check_n_setup.check_n_setup()

        elif cloud_provider == "aws":
            SYSTEM_TYPE = "aws"
            import aws_check_n_setup
            aws_check_n_setup.check_n_setup()

        USER_INPUT_DATA = get_user_input.user_input_installation()

        native_initiator(cloud_provider)

    else:
        print "\033[1;31;40m Perfotron Dashboard is already installed. " \
              "Refer Environment details under 'installation_launchpad' folder.\033[0;37;40m"
