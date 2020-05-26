import time
import re
import selenium.webdriver

from credentials import *

driver_netgear = selenium.webdriver.Chrome('./chromedriver')
driver_telia = selenium.webdriver.Chrome('./chromedriver')

def main():
    exception_sent = False
    while 1:
        try:
            start_telia()
            start_netgear()
            while 1:
                amount = poll_telia()
                if amount == -1:
                    send_sms()
                    time.sleep(180)
                elif amount < 13:
                    send_sms()
                    time.sleep(60)
                else:
                    time.sleep(60)
                if exception_sent == True:
                    send_sms('0705385996', 'Up and running again!!! Woooot!')


        except Exception as e:
            if exception_sent:
                global driver_netgear
                driver_netgear = selenium.webdriver.Chrome('./chromedriver')
                start_netgear()
                send_sms('0705385996', str(e.message) if hasattr(e, 'message') else str(e))
                exception_sent = True



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
    time.sleep(1)

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

    try:
        print('test sfind')
        element = driver_telia.find_element_by_css_selector('mybd-count-to')
        # element = driver_telia.find_element_by_class_name('mybd-number-panel__number text-number-large')
        print(element.text)
    except selenium.common.exceptions.NoSuchElementException:
        print('weeeeeeeeeeeeee')
        return amount
    driver_telia.text

    element = driver_telia.find_element_by_id('mybd-count-to')
    time.sleep(5)

    print(f'ammount {amount}')
    return amount

if __name__ == "__main__":
    main()