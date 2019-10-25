""" ===GCP Plugin to Open Required Ports (3000,8086,9003,8080)==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
# ===GCP Plugin to Open Required Ports (3000,8086,9003,8080)=="""

import sys
from subprocess import Popen, PIPE, STDOUT
import socket
import os
import ConfigParser

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname(HOSTNAME)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = ConfigParser.ConfigParser()
CONFIG.optionxform = str
CONFIG.read(os.path.join(CURRENT_DIR,"config.cnf"))


def get_command_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in cmd.stdout:
        cmd_value = line.rstrip()
    sys.stdout.flush()
    return cmd_value


def check_n_create_firewallrule(port_number, port_type, app, config):
    """ This function is called from 'open_ports' to open each port to outside"""

    if port_type == "incoming":

        check_port_incoming = config.get('GCP', 'CHECK_PORT_IN_CMD')
        check_port_incoming = check_port_incoming.replace("app", app)
        check_port_incoming = check_port_incoming.replace("port_number", port_number)

        add_port_incoming = config.get('GCP', 'ADD_PORT_IN_CMD')
        add_port_incoming = add_port_incoming.replace("app", app)
        add_port_incoming = add_port_incoming.replace("port_number", port_number)

        res = get_command_output(check_port_incoming)
        cmd = add_port_incoming

    if port_type == "outgoing":

        check_port_outgoing = config.get('GCP', 'CHECK_PORT_OUT_CMD')
        check_port_outgoing = check_port_outgoing.replace("app", app)
        check_port_outgoing = check_port_outgoing.replace("port_number", port_number)

        add_port_outgoing = config.get('GCP', 'ADD_PORT_OUT_CMD')
        add_port_outgoing = add_port_outgoing.replace("app", app)
        add_port_outgoing = add_port_outgoing.replace("port_number", port_number)

        res = get_command_output(check_port_outgoing)
        cmd = add_port_outgoing

    if port_number not in res:
        os.system(cmd)


def open_ports(config):
    """ This function is responsible for add ports to firewall- 3000, 8080, 9003, 8086 """

    check_n_create_firewallrule("3000", "incoming", "grafana", config)
    check_n_create_firewallrule("3000", "outgoing", "grafana", config)

    check_n_create_firewallrule("8080", "incoming", "jenkins", config)
    check_n_create_firewallrule("8080", "outgoing", "jenkins", config)

    check_n_create_firewallrule("9003", "incoming", "demoapi", config)
    check_n_create_firewallrule("9003", "outgoing", "demoapi", config)

    check_n_create_firewallrule("8086", "incoming", "influx", config)


def check_n_setup():
    """ Main function """
    os_type = get_command_output("python -mplatform")

    if "Ubuntu" in os_type:
        os_type = "ubuntu"

    elif 'redhat' in os_type:
        os_type = "rhel"

    elif 'centos' in os_type:
        os_type = "centos"

    gcloud_presence = get_command_output("gcloud --version")

    if "gsutil" not in gcloud_presence:
        print "gcloud sdk is essential for this installation"
        print "Please refer https://cloud.google.com/sdk/docs/ for installation"
        print "Exiting now. Retry after installing gcloud"
        sys.exit()

    gcloud_configured = get_command_output("gcloud compute instances list")
    if IP not in gcloud_configured:
        print "gcloud sdk is essential for this installation"
        print "Please refer https://cloud.google.com/sdk/docs/ for installation"
        print "Exiting now. Retry after configuring gcloud"
        sys.exit()

    get_instance_details = CONFIG.get('GCP', 'INSTANCE_DETAILS_CMD')
    get_instance_details = get_instance_details.replace("ip", IP)
    http_enabled = get_command_output(get_instance_details)

    if IP not in http_enabled:
        print "http traffic(port 80) is currently not enabled on your instance"
        print "'Allow HTTP traffic' checkbox under FireWall section has to selected"
        print "Exiting now. Retry after configuring http traffic"
        sys.exit()

    if os_type == "ubuntu":
        os.system("sudo apt-get update")
        os.system("sudo apt-get -y install python-pip")

    elif os_type == "rhel" or os_type == "centos":
        os.system("sudo yum check-update")
        os.system("sudo yum -y install python-pip")

    open_ports(CONFIG)
