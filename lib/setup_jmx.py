""" === Prepare JMX ==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
=== Prepare JMX =="""

import os


def prepare_actual_jmx(project_dir, ip_address):
    """ Main Function """

    with open(os.path.join(project_dir, 'templates',
                           'sample_demo_jmeter_script.jmx'), 'r') as sample_jmx_file:
        sample_jmx_content = sample_jmx_file.read()

    actual_jmx_content = sample_jmx_content.replace('[IP]', ip_address)

    if os.path.exists(os.path.join(project_dir, 'actual_demo_jmeter_script.jmx')):
        os.remove(os.path.join(project_dir, 'actual_demo_jmeter_script.jmx'))

    with open(os.path.join(project_dir, 'actual_demo_jmeter_script.jmx'), 'w') as jmx_file:
        jmx_file.write(actual_jmx_content)
