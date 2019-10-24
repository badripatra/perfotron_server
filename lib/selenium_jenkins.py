""" ===Selenium Script to set up first jenkins admin user==
__author__ = "Badri Patra"
__credits__ = ["Badri Patra"]
__version__ = "1.0.0"
__email__ = "badri.patra@gmail.com"
__status__ = "Testing"
===Selenium Script to set up first jenkins admin user=="""

import socket
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_jenkins_thru_browser(initial_admin_password, user_name, password, user_email, full_name):
    """ Main function """

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    display = Display(visible=0, size=(1024, 768))
    display.start()

    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False

    options = Options()
    options.add_argument("--headless")
    # --------------------Enter Admin Password-------------------------------
    jenkins_host = "http://" + ip_address + ":8080/login?from=%2F"
    driver = webdriver.Firefox(firefox_options=options)
    # driver = webdriver.Firefox()
    driver.get(jenkins_host)
    driver.implicitly_wait(120)

    input_element = WebDriverWait(driver, 240).until(EC.presence_of_element_located
                                                     ((By.NAME, "j_password")))
    input_element.send_keys(initial_admin_password)

    select_submit = driver.find_element_by_css_selector("input[type='submit']")
    select_submit.submit()

    # --------------------Enter Admin Password-------------------------------

    # --------------------Install Suggested Plugin----------------------------
    driver.implicitly_wait(120)

    install_plugin = WebDriverWait(driver, 240).until\
        (EC.presence_of_element_located
         ((By.XPATH, "//*[@id='main-panel']/div/div/div/div/div/div[2]/div/p[2]/a[1]/b")))
    install_plugin.click()

    # --------------------Install Suggested Plugin----------------------------

    # --------------------Set Admin user details----------------------------

    driver.implicitly_wait(240)

    setup_firstname = WebDriverWait(driver, 240).until(EC.presence_of_element_located
                                                       ((By.ID, "setup-first-user")))
    driver.switch_to.frame(setup_firstname)

    username = driver.find_element_by_id("username")
    username.send_keys(user_name)

    password_1 = driver.find_element_by_name("password1")
    password_1.send_keys(password)

    password_2 = driver.find_element_by_name("password2")
    password_2.send_keys(password)

    fullname = driver.find_element_by_name("fullname")
    fullname.send_keys(full_name)

    email_address = driver.find_element_by_name("email")
    email_address.send_keys(user_email)

    driver.switch_to.default_content()
    driver.find_element_by_css_selector(".btn.btn-primary.save-first-user").click()
    # --------------------Set Admin user details----------------------------

    # ---------------------------Save and Finish----------------------------
    driver.implicitly_wait(120)
    driver.switch_to.default_content()
    driver.find_element_by_css_selector(".btn.btn-link.skip-configure-instance").click()
    driver.close()
    # ---------------------------Save and Finish----------------------------

    display.stop()

    return "yes"


with open("/var/lib/jenkins/secrets/initialAdminPassword", "r") as details_file:
    SECRET_CODE = details_file.read().strip()

setup_jenkins_thru_browser(SECRET_CODE, "admin", "admin", "admin@admin.com", "admin")
