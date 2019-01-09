###################
# @owner SMSFIRE ##
# #################

from datetime import datetime
from time import sleep
from time import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import socket
import urllib.request

message_text='Your message' # message
no_of_message=1 # no. of time
moblie_no_list = ["5511944556677","5511966991155"] # list of phone number with international prefix

def element_presence(by,xpath,time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except :
        is_connected()

### SAVE QRCODE - START ###
### Create folder qrcodes in the same path
def get_qrcode():
    img = driver.find_element_by_xpath('//div[@class="_2EZ_m"]/img')
    src = img.get_attribute('src')
    urllib.request.urlretrieve(src, "./qrcodes/"+str(time())+".png")
    print("Scan QRCODE")
    sleep(5) #whatsapp update his qrcode every 20 seconds
    
    # CHECK If QRCode still valid, if not update it
    try:
        element_presence(By.XPATH,'//span[@data-icon="refresh-l-light"]',2)
        refresh = driver.find_element_by_xpath('//span[@data-icon="refresh-l-light"]')
        refresh.click()
    except:
        pass        
    # CHECK If whatsapp web were pared
    try:
        element_presence(By.CLASS_NAME,'_2Uo0Z',5)
        print("Whatsapp pared with server")
    except:
        get_qrcode()
### SAVE QRCODE - END ###

### CALL WHATSAPP API - start ###
def send_whatsapp_msg(phone_no,text):
    driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no)) #Call official whatsapp api
    #Each request the server popup alert - this make automatic click on this
    try:
        alert = browser.switch_to.alert
        alert.dismiss()
    except Exception as e:
        pass
    finally:
        print("Message sent "+str(phone_no)+" as "+str(time()))
### CALL WHATSAPP API - end ###
    #Search for text box and send button
    try:
        element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        txt_box = driver.find_element(By.CLASS_NAME, '_2S1VP')
        txt_box.send_keys(text)
        txt_box.send_keys("\n")
        button = driver.find_element_by_class_name('_35EW6')
        button.click()

    except Exception as e:
        get_qrcode()

    finally:
        alert = browser.switch_to.alert
        alert.accept()

######################### STAR SERVER ##############################
#Infinit loop throug numbers
#This is perfect for dinamyc lists but should be coded
while True:

    if not moblie_no_list:
        print('Without number to sent')
        sleep(5)

    else:
        optionss = webdriver.ChromeOptions();
        optionss.add_argument('--user-data-dir=./User_Data')
        driver = webdriver.Chrome(options=optionss)
        driver.get("http://web.whatsapp.com")
        sleep(5) #wait time to scan the code in second

        # Re-check if sync were active - start
        try:
            element_presence(By.XPATH,'//div[@class="_2EZ_m"]/img',15)
            get_qrcode()
        except Exception as e:
            pass
        # Re-check if sync were active - start

        for moblie_no in moblie_no_list:
            try:
                send_whatsapp_msg(moblie_no,message_text)
            except Exception as e:
                sleep(5)
                is_connected()
            finally:
                print("Message sent to "+str(moblie_no)+" at "+str(time()))
                sleep(1)
                #Check if we have the ack of read or not
                try:
                    element_presence(By.XPATH,'//span[@data-icon="msg-dblcheck-ack"]',3)
                    print("Delivered with ack of read to "+str(moblie_no)+" at "+str(time()))
                except Exception as e:
                    print("Delivered without ack of read to "+str(moblie_no)+" at "+str(time()))
                    sleep(1)

    #close window and restart the process using the same session_id
    driver.close()
