from time import sleep
from platform import system
from getpass import getuser
from selenium import webdriver
from subprocess import (Popen, PIPE, run)
from typing import (Union, List, Optional, Any)
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver() -> webdriver:
    """
    https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html
    Search for LAST_CHANGE
    """
    chrome_options: webdriver.chrome.options.Options = Options()
    chrome_options.headless = True
    if operating_system() == "Windows":
        path_to_script: str = sys_output(f"cd \\Users\\{user_name()} && dir /s /b chromedriver.exe")
        chrome_options.binary_location = sys_output(f"cd \\Users\\{user_name()} && dir /s /b chromium.exe")
    else:
        path_to_script: str = sys_output("mdfind", "-name", "chromium_selenium")
        chrome_options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
    return webdriver.Chrome(path_to_script, options=chrome_options)


def check_xpath_element(driver: webdriver, xpath: str) -> Optional[Any]:
    try:
        element: webdriver.remote = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(("xpath", xpath)))
    except TimeoutException:
        print("\nElement(By.XPATH" + ", " + xpath + ") does not exist or is out of reach.")
        return None

    return element


def check_xpath_elements(driver: webdriver, xpath: str) -> Optional[Any]:
    try:
        elements: webdriver.remote = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located(("xpath", xpath)))
    except TimeoutException:
        print("\nElements(By.XPATH" + ", " + xpath + ") does not exist or is out of reach.")
        return None

    return elements


def scroll_down(driver: webdriver, scroll_value: int = 325) -> None:
    sleep(0.5)
    driver.execute_script("window.scrollTo(0, window.scrollY + {});".format(scroll_value))
    sleep(0.5)


def quit_chromium(driver: webdriver) -> None:
    driver.quit()
    if operating_system() != "Windows":
        run(['osascript', '-e', 'quit app \"Chromium\"'])


def operating_system() -> str:
    return system()


def user_name() -> str:
    return getuser()


def sys_output(*cmd) -> Union[str, List[str]]:
    if operating_system() == "Windows":
        p: Popen = Popen(cmd[0], shell=True, stdout=PIPE)
    else:
        p: Popen = Popen(cmd, stdout=PIPE)
    output: List[str] = p.communicate()[0].decode("ascii").strip().split("\n")
    if len(output) == 1:
        return output[0]
    else:
        return output
