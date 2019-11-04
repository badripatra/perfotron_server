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
import socket
import argparse
import datetime
from xml.etree import ElementTree as ET


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(CURRENT_DIR + '/lib'))
os.chdir(CURRENT_DIR)

HOME = os.path.expanduser("~")


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
    print "6. selenium (python module)"
    print "7. pyvirtualdisplay (python module)"

    os.system(cmd)

    print "-----------------Resolving Dependencies------------------------------"


def get_ip():
    """ This function is responsible to identify clouder provider from BIOS """

    if 'Google' in BIOS_TYPE or 'amazon' in BIOS_TYPE:
        ip_address = get_command_output("curl -s ifconfig.me")
    else:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

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


def add_backend_listner():
    """ This function is responsible for adding back end listener to a existing jmx"""

    with open(os.path.join(CURRENT_DIR, 'docs_and_templates',
                           'backend_listner.jmx')) as backend_listner:
        backend_listner_data = str(backend_listner.read()).replace("[IP]", IP)

    with open('backend_listner.jmx', "w") as backend_listner:
        backend_listner.write(backend_listner_data)

    backend_listener = ET.parse("backend_listner.jmx")

    base_script = ET.parse(ARGS.jmx)
    existing_struct = base_script.find("./hashTree/hashTree")
    new_condition = backend_listener.getroot()
    existing_struct.append(new_condition)

    os.system("mkdir -p ~/user_jmx_run_results")

    file_name = os.path.join(HOME, "user_jmx_run_results", os.path.basename(ARGS.jmx))

    with open(file_name, "w") as user_jmx:
        user_jmx.write(ET.tostring(base_script.getroot()))

    os.system("rm -rf backend_listner.jmx")

    return file_name


def uninstall_perftool(package_manager):
    """ This function is responsible for uninstalling Perfotron dashboard"""

    print "Started Uninstalling the perf tool"

    print "-------------------Progress-----------------------------------------------"

    if package_manager == "rpm":

        os.system("sudo yum -y remove grafana >> ~/un-installation_details.log 2>&1")
        print "Removed Grafana Server"

        os.system("sudo yum -y remove influxdb >> ~/un-installation_details.log 2>&1")
        print "Removed Influx DB"

        # os.system("sudo yum -y remove jenkins >> ~/un-installation_details.log 2>&1")
        # print "Removed Jenkins"

        os.system("sudo yum clean all >> ~/un-installation_details.log 2>&1")

    elif package_manager == "dpkg":

        os.system("sudo apt-get purge remove grafana >> ~/un-installation_details.log 2>&1")
        print "Removed Grafana Server"

        os.system("sudo apt-get purge remove influxdb >> ~/un-installation_details.log 2>&1")
        print "Removed Influx DB"

        # os.system("sudo apt-get purge remove jenkins >> ~/un-installation_details.log 2>&1")
        # print "Removed Jenkins"

        os.system("sudo apt-get clean >> ~/un-installation_details.log 2>&1")

    print "Stopped Demo API"
    os.system("kill -9 `ps -ef|grep -v grep|grep 'python demo_api.py'"
              "|awk '{print $2}'` > /dev/null 2>&1")

    # print "Killing existing instances of jenkins"
    ''' os.system("kill $(ps aux | grep -v grep| grep 'jenkins' | "
                  "awk '{print $2}') >> ~/un-installation_details.log 2>&1") '''

    print "Killing existing instances of influx, grafana"
    os.system("kill $(ps aux | grep -v grep| grep 'influx' | "
              "awk '{print $2}') >> ~/un-installation_details.log 2>&1")
    os.system("kill $(ps aux | grep -v grep| grep 'grafana' | "
              "awk '{print $2}') >> ~/un-installation_details.log 2>&1")

    # print "Removing Files and Folder related to jenkins"
    # os.system("sudo rm -rf /var/lib/jenkins >> ~/un-installation_details.log 2>&1")

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


def native_initiator(install_jenkins):
    """ This function is responsible for copying required files to
    installation directory and start the run"""

    os.system("mkdir -p ~/installation_launchpad")

    os.system("cp -r os_specific_files/"+OS_TYPE+"/*.* ~/installation_launchpad")

    os.system ("cp requirements.txt ~/installation_launchpad")

    os.system("cp -r grafana/*.* ~/installation_launchpad")

    os.system("cp docs_and_templates/sample_demo_jmeter_script.jmx "
              "~/installation_launchpad/actual_demo_jmeter_script.jmx")

    os.system('sed -i -e "s/IP_ADDRESS/'+IP+'/g" ~/installation_launchpad'
                                            '/actual_demo_jmeter_script.jmx')

    os.system("cp lib/demo_api.py ~/installation_launchpad")

    os.system("cp demo_api/invoke_restapis.sh ~/installation_launchpad")

    os.system("cp setup_details/details_template.yaml ~/installation_launchpad")

    os.system("cp server_stats/invoke_serverstats.sh ~/installation_launchpad")

    os.system("cp server_stats/server_stats.ini ~/installation_launchpad")

    os.system("cp lib/system_monitor.py ~/installation_launchpad")

    os.system("cp lib/config/config.cnf ~/installation_launchpad")


    if install_jenkins == "true":
        os.system("cp jenkins/jenkins_job_setup.sh ~/installation_launchpad")
        os.system("cp jenkins/config.xml ~/installation_launchpad")
        os.system("cp lib/native.py  ~/installation_launchpad")
        os.system("cp lib/selenium_jenkins.py  ~/installation_launchpad")
        os.system("cp jenkins/unlock_jenkins.sh ~/installation_launchpad")
        os.system("cp setup_details/details_template.yaml ~/installation_launchpad")
        os.system("sudo python ~/installation_launchpad/native.py install_jekins:true")
    else:
        os.system("cp lib/native.py  ~/installation_launchpad")
        os.system("cp apache-jmeter-5.1.1.tgz ~/installation_launchpad")
        os.system("sudo tar -xf  ~/installation_launchpad/apache-jmeter-5.1.1.tgz"
                  " -C ~/installation_launchpad")

        os.chdir(HOME)
        os.system("sudo python ~/installation_launchpad/native.py install_jekins:false")

    os.system("sudo chown `id -un`:`id -gn` ~/installation_launchpad/*.*")


if __name__ == '__main__':

    signal.signal(signal.SIGINT, sigint_handler)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--uninstall", help="Uninstall Software Stack", action="store_true")
    PARSER.add_argument("--jmx",
                        help="Jmeter Test Plan name with complete path to be executed."
                             " Example: python perfenv_e2e --jmx sample_user_testplan.jmx")
    ARGS = PARSER.parse_args()

    BIOS_TYPE = get_command_output("sudo dmidecode -s bios-version")
    IP = get_ip()
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

        if ARGS.jmx or ARGS.uninstall:
            print "\033[1;33;40m '--jmx' or '--uninstall' " \
                  "options are only possible after Perfotron Dashboard is installed"

            print " Run 'python perfotron' command to install the Perfotron Dashboard"
            print " Exiting now\033[0;37;40m"
            sys.exit()

        else:
            with open(os.path.join(CURRENT_DIR, 'docs_and_templates', 'About.txt')) as About:
                print About.read()

            dependency_resolution()  # Install all dependent modules

    if ARGS.jmx and ARGS.uninstall:

        print "\033[1;33;40m '--jmx' and '--uninstall' options can not selected together."
        print " Select '--uninstall' to remove the tool from your system"
        print " Select '--jmx' to enable your Jmeter Script to run and reflect in Perfotron Dashboard"
        print " Exiting Now\033[0;37;40m"

        sys.exit()

    if ARGS.jmx:

        if "/" not in ARGS.jmx:
            ARGS.jmx = os.path.join(os.getcwd(), "..", ARGS.jmx)

        if not os.path.exists(ARGS.jmx):
            print "\033[1;31;40m Input JMX : "+ARGS.jmx+" does not exist.\033[5;37;40m"

            print "Check the location of the path and then retry.Exiting now."

            sys.exit()

        print "------------------Started Executing Jmeter Script ------------------------------"

        JMX_FILE = add_backend_listner()

        RESULT_FOLDER = str(datetime.datetime.now())
        RESULT_FOLDER = RESULT_FOLDER.replace(" ", "_")
        RESULT_FOLDER = RESULT_FOLDER.replace(":", "-")
        RESULT_FOLDER = RESULT_FOLDER.replace(".", "-")

        RESULT_FOLDER = HOME + "/user_jmx_run_results/"+RESULT_FOLDER

        os.system("mkdir -p " + RESULT_FOLDER)
        os.chdir(RESULT_FOLDER)

        CMD_JMX = "~/installation_launchpad/apache-jmeter-5.1.1/bin/jmeter -n -t " + JMX_FILE

        print "Command Triggered :" + CMD_JMX
        print "Perfdashboard URL : "\
              + "http://" + IP + ":3000/d/sample_dashboard/performance-dashboard?orgId=1\n"

        os.system("~/installation_launchpad/apache-jmeter-5.1.1/bin/jmeter -n -t " + JMX_FILE)
        print "\nJmeter Test result location : " + RESULT_FOLDER + "\n"
        print "---------------------Finished Executing Jmeter Script -----------------------------"
        sys.exit()

    import get_user_input   # Import user input lib

    if ARGS.uninstall:
        get_user_input.user_input_uninstallation()
        uninstall_perftool(PACKAGE_MANAGER)
        sys.exit()

    if not PERF_DASHBOARD:

        if 'Google' in BIOS_TYPE:
            SYSTEM_TYPE = "google_cloud"
            import google_cloud_check_n_setup
            google_cloud_check_n_setup.check_n_setup()

        elif 'amazon' in BIOS_TYPE:
            SYSTEM_TYPE = "aws"
            import aws_check_n_setup
            aws_check_n_setup.check_n_setup()

        USER_INPUT_DATA = get_user_input.user_input_installation()

        if USER_INPUT_DATA["jenkins"] == "yes":
            INSTALL_JENKINS = "true"
        else:
            INSTALL_JENKINS = "false"

        native_initiator(INSTALL_JENKINS)

    else:
        print "\033[1;31;40m Perfotron Dashboard is already installed. " \
              "Refer Environment details under 'installation_launchpad' folder.\033[0;37;40m"
