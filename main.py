import time
import re
import selenium.webdriver
import datetime

from credentials import *
from selenium.webdriver.chrome.options import Options

co = Options()
driver_netgear = None
driver_telia = None

#driver_netgear = selenium.webdriver.Chrome('./chromedriver')

def main():
    exception_sent = False
    global co
    global driver_netgear
    global driver_telia

    co.add_argument('--headless')
    driver_netgear = selenium.webdriver.Chrome('./chromedriver', options=co)
    driver_telia = selenium.webdriver.Chrome('./chromedriver', options=co)
    
    while 1:
        try:
            print('Startup')
            start_telia()
            start_netgear()
            print('Startup done')
            while 1:
                sleeptime = 180
                print(f'Start seq. @ time: {datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")}')
                print('Get data left...')
                amount = poll_telia()
                print(f'{amount} Gb data left')
                if amount < 0:
                    print(f'{amount} is to damn small')
                    send_sms()
                    sleeptime = 77
                elif amount < 19.77:
                    print(f'Running out ({amount}) have to refill')
                    send_sms()
                    if amount < 5:
                        sleeptime = 60
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
                driver_netgear = selenium.webdriver.Chrome('./chromedriver', options=co)
                start_netgear()
                send_sms(phone_nr, str(e.message) if hasattr(e, 'message') else str(e))
                exception_sent = True
            time.sleep(60)


def start_netgear():
    print('Netgear start')
    global driver_netgear
    global username_netgear
    global password_netgear

    driver_netgear.get('http://192.168.65.1')
    print('username')
    element = driver_netgear.find_element_by_id('user_name')
    element.send_keys(username_netgear)
    time.sleep(20)
    print('password')
    element = driver_netgear.find_element_by_id('session_password')
    element.send_keys(password_netgear)
    print('logging in')
    element.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    print('Done')


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
    print('Telia start')
    global driver_telia
    global username_telia
    global password_telia

    amount = 0

    driver_telia.get('https://www.telia.se/foretag/mybusiness/login')
    driver_telia.refresh()
    #time.sleep(4)
    print('accpting cookies')
    element = driver_telia.find_element_by_id('cookie-preferences-accept-button')
    element.click()
    #time.sleep(1)
    print('username')
    element = driver_telia.find_element_by_id('username')
    element.send_keys(username_telia)
    print('password')
    element = driver_telia.find_element_by_id('login-simple-password')
    element.send_keys(password_telia)
    print('logging in')
    element.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    #time.sleep(4)
    print('Done')

def poll_telia():
    global driver_telia
    amount = -1
    
    print('reflesh telia and wait 5s')
    driver_telia.refresh()
    time.sleep(5)    
    
    try:
        print('Finding web element')
        element = driver_telia.find_element_by_css_selector('mybd-count-to')
    except selenium.common.exceptions.NoSuchElementException:
        print('Did not find web element')
        return amount
    return float(element.text)

if __name__ == "__main__":
    main()
