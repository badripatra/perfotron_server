""" ===AWS Plugin to Open Required Ports (3000,8086,9003,8080)==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
# ===AWS Plugin to Open Required Ports (3000,8086,9003,8080)=="""


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
CONFIG.read(os.path.join(CURRENT_DIR, "config", "config.cnf"))

CHECK_PORT = CONFIG.get('AWS', 'CHECK_PORT_CMD')
ADD_PORT = CONFIG.get('AWS', 'ADD_PORT_CMD')


def get_command_output(command):
    """ This function is responsible for running a command on Shell & return output"""
    cmd = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    for line in cmd.stdout:
        cmd_value = line.rstrip()
    sys.stdout.flush()
    return cmd_value


def check_n_create_firewall_rule(port_number, port_type, security_group_name, security_group_id):
    """ This function is responsible for check and add a port in aws security group"""

    if port_type == "incoming":

        cmd_check_port = CHECK_PORT.replace("port_type", 'IpPermissions[]')
        cmd_check_port = cmd_check_port.replace("gid", security_group_id)
        cmd_check_port = cmd_check_port.replace("port_number", port_number)
        res = get_command_output(cmd_check_port)

        cmd = ADD_PORT.replace("type", "ingress")
        cmd = cmd.replace("sgname", security_group_name)
        cmd = cmd.replace("port_no", port_number)

    if port_type == "outgoing":

        cmd_check_port = CHECK_PORT.replace("port_type", 'IpPermissionsEgress[]')
        cmd_check_port = cmd_check_port.replace("gid", security_group_id)
        cmd_check_port = cmd_check_port.replace("port_number", port_number)
        res = get_command_output(cmd_check_port)

        cmd = ADD_PORT.replace("type", "egress")
        cmd = cmd.replace("sgname", security_group_name)
        cmd = cmd.replace("port_no", port_number)

    if port_number not in res:
        os.system(cmd)


def open_ports(security_group_name, security_group_id):
    """ This function is responsible to open ports 3000, 8080, 9003, 8086 in aws security group"""

    check_n_create_firewall_rule("3000", "incoming", security_group_name, security_group_id)
    check_n_create_firewall_rule("3000", "outgoing", security_group_name, security_group_id)

    # check_n_create_firewall_rule("8080", "incoming", security_group_name, security_group_id)
    # check_n_create_firewall_rule("8080", "outgoing", security_group_name, security_group_id)

    check_n_create_firewall_rule("9003", "incoming", security_group_name, security_group_id)
    check_n_create_firewall_rule("9003", "outgoing", security_group_name, security_group_id)

    check_n_create_firewall_rule("8086", "incoming", security_group_name, security_group_id)


def check_n_setup():
    """ Main Function. Checks the os_type, aws-cli availabilty and configuration.
     Then opens required ports """

    os_type = get_command_output("python -mplatform")

    if "Ubuntu" in os_type:
        os_type = "ubuntu"

    elif 'redhat' in os_type:
        os_type = "rhel"

    elif 'centos' in os_type:
        os_type = "centos"

    elif 'amz' in os_type:
        os_type = "amazon-linux"

    aws_presence = get_command_output("aws --version")

    if "aws-cli" not in aws_presence:
        print "aws cli is currently not installed on your instance"
        print "Refer https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html"
        print "Exiting now. Retry after installing aws cli"
        sys.exit()

    aws_cli = get_command_output("aws ec2 describe-instances|grep 'PrivateIpAddress'| head -1")
    if IP not in aws_cli:
        print "aws cli is not configured on your instance"
        print "Refer https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html"
        print "Exiting now. Retry after configuring aws cli"
        sys.exit()

    if os_type == "ubuntu":
        os.system("sudo apt-get update")
        os.system("sudo apt-get -y install python-pip")
        os.system("sudo apt-get -y install python-minimal")

    elif os_type == "rhel" or os_type == "centos" or os_type == "amazon-linux":
        os.system("sudo yum check-update")
        os.system("sudo yum -y install python-pip")

    instance_id = get_command_output('cat /var/lib/cloud/data/instance-id')

    cmd_get_security_group_name = CONFIG.get('AWS', 'GET_SG_NAME_CMD')
    cmd_get_security_group_name = cmd_get_security_group_name.replace("inst_id", instance_id)
    security_group_name = get_command_output(cmd_get_security_group_name)

    cmd_get_security_group_id = CONFIG.get('AWS', 'GET_SG_ID_CMD')
    cmd_get_security_group_id = cmd_get_security_group_id.replace("inst_id", instance_id)
    security_group_id = get_command_output(cmd_get_security_group_id)

    open_ports(security_group_name, security_group_id)
