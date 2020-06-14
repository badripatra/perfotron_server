from datetime import datetime, timedelta
import re
import subprocess
import sys
from operator import itemgetter
import csv
import json
import os
import collections
import time

reload(sys)
sys.setdefaultencoding('utf8')


# -----------------------------------------Functions--------------------------------------------------------------------

def convert_csv_to_json(content, user_csv_file, format):  # Convert csv data into json and write it

    csv_row = collections.OrderedDict()
    csv_rows_list = []

    epoch_time = str(int(time.time()))

    converted_json_name = user_csv_file.replace(".csv", ".json")

    with open(user_csv_file, "w") as user_csv:
        user_csv.write(content)

    with open(user_csv_file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            csv_row = collections.OrderedDict(sorted(row.items(), key=lambda item: reader.fieldnames.index(item[0])))
            csv_rows_list.append(csv_row)

        write_json(csv_rows_list, converted_json_name, format)

    return converted_json_name


def write_json(data, json_file, format):  # write file as json

    for each_item in data:
        for k, v in each_item.iteritems():
            each_item[k] = v.strip()

    with open(json_file, "w") as json_testcase:
        if format == "pretty":
            json_testcase.write(json.dumps(data, sort_keys=False, indent=4,
                                           separators=(',', ': '), encoding="utf-8", ensure_ascii=False))
        else:
            json_testcase.write(json.dumps(data))


def generate_performance_scenario_json(content, user_csv_file):  # Generate Performance_scenario json from csv
    output_file_name = convert_csv_to_json(content, user_csv_file, 'pretty')
    return output_file_name


def get_dates(date_requirement):  # Get start and end dates

    date_value_list = date_requirement.split("-")

    if len(date_value_list) > 1:
        date_delta = date_value_list[1]
        date_value = (datetime.today() - timedelta(days=int(date_delta))).strftime('%Y-%m-%d')
    else:
        date_value = (datetime.today()).strftime('%Y-%m-%d')

    return date_value


def get_command_output(command):
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_value = str(cmd.stdout.readlines()[0]).strip()  # Read command output
    sys.stdout.flush()
    return cmd_value


# -----------------------------------------Functions--------------------------------------------------------------------

# ------------------------------Generate test case jmx by substituting values in sample jmx ----------------------------


class create_jmx_scenario():  # Initialization class

    def __init__(self, content, user_csv_file, file_name):

        output_json_name = generate_performance_scenario_json(content, user_csv_file)

        with open(output_json_name, 'r') as json_data:
            performance_testcases_input = json.load(json_data)

        self.output_jmx_name = file_name

        self.performance_testcases_input = performance_testcases_input
        self.pattern_to_identify_jmx_input_fields = r'(?<=\[).+?(?=\])'

    def get_content(self, file):
        with open(os.path.join(file)) as file_name:
            file_content = file_name.read()
        return file_content

    def form_jmx_file(self):

        testscenario_list = []

        performance_testcases = sorted(self.performance_testcases_input, key=itemgetter('Thread_Group_Name'))

        for each_row in performance_testcases:
            testscenario_name = each_row["Thread_Group_Name"]
            if testscenario_name not in testscenario_list:
                testscenario_list.append(testscenario_name)

        testscenario_json = {}

        for testscenario in testscenario_list:
            testscenario_steps = []
            for each_row in self.performance_testcases_input:
                testscenario_name = each_row["Thread_Group_Name"]
                if testscenario_name == testscenario:
                    testscenario_steps.append(each_row)

            testscenario_json[testscenario] = testscenario_steps

        testplan_content = self.get_content("testplan_sampler")
        threadgroup_content_list = ""

        for each_scenario in testscenario_list:

            threadgroup_content = self.get_content("threadgroup_sampler")
            threadgroup_content = threadgroup_content.replace("[testscenario_name]", each_scenario)

            concurrent_users = 0
            ramp_up_in_seconds = 0
            duration_in_seconds = 0

            Data = ""

            for each_testcase in testscenario_json[each_scenario]:

                header_values_collective = ""
                loop_tag = ""
                testcase_name = str(each_testcase['HTTP_Request'])
                jmeter_component_type = str(each_testcase['Method'])
                execution_control = str(each_testcase['Execution_Control'])

                if (execution_control == 'yes'):
                    Url = str(each_testcase['url'])

                    concurrent_users_tc = str(each_testcase['Number of Users'])
                    concurrent_users = concurrent_users + int(concurrent_users_tc)

                    ramp_up_in_seconds_tc = str(each_testcase['Ramp-up_period_Seconds'])
                    ramp_up_in_seconds = ramp_up_in_seconds + int(ramp_up_in_seconds_tc)

                    duration_in_seconds_tc = str(each_testcase['Duration_in_Seconds'])
                    duration_in_seconds = duration_in_seconds + int(duration_in_seconds_tc)

                    POST_params = str(each_testcase['POST_params'])

                    responsetime_threshold_in_ms = str(each_testcase["Duration_Assertion_Milliseconds"])

                    header_tags = re.findall(self.pattern_to_identify_jmx_input_fields,
                                             str(each_testcase['Header_Manager']))

                    for each_header in header_tags:
                        header_values = self.get_content("element_property_sampler")

                        header_name = str(each_header).split(":")[0]
                        header_value = str(each_header).split(":")[1]

                        header_values = header_values.replace("[header_name]", header_name)
                        header_values = header_values.replace("[header_value]", header_value)

                        header_values_collective = header_values_collective + header_values

                    JMX_ThreadGroup_Content = self.get_content(jmeter_component_type)
                    input_jmx_tags = re.findall(self.pattern_to_identify_jmx_input_fields,
                                                JMX_ThreadGroup_Content)

                    for each_jmx_tag in input_jmx_tags:
                        # Replace the input tags in jmx with variable values
                        JMX_ThreadGroup_Content = JMX_ThreadGroup_Content.replace("[" + each_jmx_tag + "]",
                                                                                  eval(each_jmx_tag))

                    Data = Data + JMX_ThreadGroup_Content

            threadgroup_content = threadgroup_content.replace("[sampler_data]", Data)

            input_jmx_tags = re.findall(self.pattern_to_identify_jmx_input_fields,
                                        threadgroup_content)

            for each_jmx_tag in input_jmx_tags:
                # Replace the input tags in jmx with variable values
                threadgroup_content = threadgroup_content.replace("[" + each_jmx_tag + "]",
                                                                          eval(each_jmx_tag))

            threadgroup_content_list = threadgroup_content_list + threadgroup_content

        testplan_content = testplan_content.replace('replace_content', threadgroup_content_list)

        with open(self.output_jmx_name, "w") as user_jmx:
            user_jmx.write(testplan_content)




# ------------------------------Generate test case jmx by substituting values in sample jmx ----------------------------