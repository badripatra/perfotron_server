""" ===Users inputs for proceeding  with Perf Dashboard Installation==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
===Users inputs for proceeding  with Perf Dashboard Installation=="""

import sys
import inquirer


def user_input_installation():
    """ This function is responsible for taking user input before setting up perfotron dashboard"""

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


    # -------------------------------------------------------------------------------------------- #

    return user_choice


def user_input_uninstallation():
    """ This function is responsible for taking user input before uninstalling up perfotron dashboard"""

    user_choice = {}

    # ---------------------------------------------------------------------------------------- #

    uninstllation_perfotron_dashboard = [
        inquirer.List('confirmation',
                      message="Do you want to uninstall perfotron dashboard ? ",
                      choices=['yes', 'no'])]

    user_selection_perf_dashboard = inquirer.prompt(uninstllation_perfotron_dashboard)

    # ------------------------------------------------------------------------------------------ #

    # ------------------------------------------------------------------------------------------- #

    if user_selection_perf_dashboard["confirmation"] == 'no':
        print "Exiting, as you selected not to proceed with un-installation."
        sys.exit()

    # -------------------------------------------------------------------------------------------- #

    return user_choice
