import time
import re
import selenium.webdriver
import datetime

from credentials import *

#driver_netgear = selenium.webdriver.Chrome('./chromedriver')
driver_netgear = selenium.webdriver.Chrome()
driver_telia = selenium.webdriver.Chrome()

def main():
    exception_sent = False
    while 1:
        try:
            print('Startup')
            start_telia()
            start_netgear()
            print('Startup done')
            while 1:
                sleeptime = 60
                print(f'Start seq. @ time: {datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")}')
                print('Get data left...')
                amount = poll_telia()
                print(f'{amount} Gb data left')
                if amount < 0:
                    print(f'{amount} is to damn small')
                    send_sms()
                    sleeptime = 180
                elif amount < 19.9:
                    print(f'Running out ({amount}) have to refill')
                    send_sms()
                else:
                    print('It\'s ok')
                if exception_sent == True:
                    send_sms(phone_nr, 'Up and running again!!! Woooot!')
                    exception_sent = False
                print(f'Will start again in {sleeptime} s')
                time.sleep(sleeptime)


        except Exception as e:
            if not exception_sent:
                print(e)
                global driver_netgear
                driver_netgear = selenium.webdriver.Chrome('./chromedriver')
                start_netgear()
                send_sms(phone_nr, str(e.message) if hasattr(e, 'message') else str(e))
                exception_sent = True
            time.sleep(60)


def start_netgear():
    global driver_netgear
    global username_netgear
    global password_netgear

    driver_netgear.get('http://192.168.65.1')
    time.sleep(1)
    element = driver_netgear.find_element_by_id('user_name')
    element.send_keys(username_netgear)
    time.sleep(1)
    element = driver_netgear.find_element_by_id('session_password')
    element.send_keys(password_netgear)
    element.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    time.sleep(1)

def send_sms(number: str = '4466', sms: str = 'fortsätt'):
    global driver_netgear
    element = driver_netgear.find_element_by_id('button_compose_sms')
    element.click()
    time.sleep(1)
    element = driver_netgear.find_element_by_id('sms_send_recipient_field')
    element.send_keys(number)
    time.sleep(1)
    element = driver_netgear.find_element_by_id('sms_send_message_field')
    element.send_keys(sms)
    element.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    print('Sms sent')

def start_telia():
    global driver_telia
    global username_telia
    global password_telia

    amount = 0

    driver_telia.get('https://www.telia.se/foretag/mybusiness/login')
    driver_telia.refresh()
    time.sleep(4)
    element = driver_telia.find_element_by_id('cookie-preferences-accept-button')
    element.click()
    time.sleep(1)
    element = driver_telia.find_element_by_id('username')
    element.send_keys(username_telia)
    element = driver_telia.find_element_by_id('login-simple-password')
    element.send_keys(password_telia)
    element.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    time.sleep(4)

def poll_telia():
    global driver_telia
    amount = -1
    
    driver_telia.refresh()

    try:
        print('Finding web element')
        element = driver_telia.find_element_by_css_selector('mybd-count-to')
    except selenium.common.exceptions.NoSuchElementException:
        print('Did not find web element')
        return amount
    return float(element.text)

if __name__ == "__main__":
    main()