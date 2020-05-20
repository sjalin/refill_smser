import time
import re
import selenium.webdriver

driver_netgear = selenium.webdriver.Chrome('/home/sebbe/projects/super_smser/chromedriver')
#driver_telia = selenium.webdriver.Chrome('/home/sebbe/projects/super_smser/chromedriver')


def main():
    #start_telia()
    start_netgear()
    while 1:
     #   amount = poll_telia()
        amount = -1
        if amount == -1:
            send_sms()
            time.sleep(180)
        elif amount < 13:
            send_sms()
            time.sleep(60)
        else:
            time.sleep(60)


def start_netgear():
    global driver_netgear
    username_netgear = ''
    password_netgear = ''
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

    username_telia = ''
    password_telia = ''
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

    try:
        element = driver_telia.find_element_by_id('97d3cdac-97cf-43e1-9144-207cd15696ad')
        # element = driver_telia.find_element_by_class_name('mybd-number-panel__number text-number-large')
        print(element.text)
    except selenium.common.exceptions.NoSuchElementException:
        return -1
    #     < div
    #
    #     class ="mybd-number-panel__number text-number-large" >
    #
    #     < mybd - count - to
    #     value = "5.46"
    #     aria - label = "5.46" > 5.46 < / mybd - count - to >
    #
    # < / div >
    """    < mybd - count - to
        value = "5.94"
        aria - label = "5.94" > 5.94 < / mybd - count - to >
        """
    """    < mybd - count - to
        value = "6"
        aria - label = "5.94" > 5.94 < / mybd - count - to >
        """
    element = driver_telia.find_element_by_id('mybd-count-to')
    time.sleep(5)

    return amount

if __name__ == "__main__":
    main()

getGB = re.compile(r'" > (\d).(\d\d) < / mybd - count - to >')
test = """    < mybd - count - to
    value = "5.94"
    aria - label = "5.94" > 5.94 < / mybd - count - to >
    """
gb = getGB.search(test)
print(gb.groups())
