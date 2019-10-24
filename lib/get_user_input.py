""" ===Users inputs for proceeding  with Perf Dashboard Installation==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
===Users inputs for proceeding  with Perf Dashboard Installation=="""

import sys
import inquirer


def user_input():
    """ This function is responsible for taking user input before setting up perf dashboard"""

    user_choice = {}
    print "\nPlease answer the questions below to get started \n"

    # ---------------------------------------------------------------------------------------- #

    set_up_perf_dashboard = [
        inquirer.List('Perf_Dashboard',
                      message="Would you like to go ahead for installations of perf dashboard ? ",
                      choices=['yes', 'no'])]

    user_selection_perf_dashboard = inquirer.prompt(set_up_perf_dashboard)
    user_choice["set_up_perf_dashboard"] = user_selection_perf_dashboard["Perf_Dashboard"]

    # ------------------------------------------------------------------------------------------ #

    # ------------------------------------------------------------------------------------------- #

    if user_selection_perf_dashboard["Perf_Dashboard"] == 'no':
        print "Exiting, as you selected not to proceed with installation."
        sys.exit()

    sample_run_jenkins = [inquirer.List('jenkins',
                                        message="Do you want the demo be triggered from jenkins ?",
                                        choices=['yes', 'no'])]

    user_selection_jenkins_vs_local = inquirer.prompt(sample_run_jenkins)
    user_choice["jenkins"] = user_selection_jenkins_vs_local["jenkins"]

    # -------------------------------------------------------------------------------------------- #

    return user_choice
