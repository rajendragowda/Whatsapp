import time
from webwhatsapi import WhatsAPIDriver
from datetime import datetime
from random import randint
import os
import webwhatsapi
from email import message

csv_file_name = 'chat_log.csv'
images_folder = 'Images'
qr_filename = 'qr_code.png'
poll_period = 3
group_name = webwhatsapi.chat_grp_string

def get_img_path():
    rand = str(randint(0, 100))
    time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_filename = time_stamp + rand + '.jpg'
    img_dir = dir_path + '\\Images'
    return (img_dir, img_filename)

try:
    driver = WhatsAPIDriver()
    driver.setup_excel(csv_file_name)
    driver.setup_image(images_folder)
 
    while True:
        time.sleep(poll_period)
        
        for contact in driver.get_unread():
            
            group_name = str(contact.chat.name)
            for message in contact.messages:
                if (message._js_obj[u'type'] == 'chat'):
                    curr_msg = str(message.safe_content)
                else: 
                    curr_msg = str(message.content) # current message    
                msg_sender = str(message.sender) # Sender name
                timestamp = str(message.timestamp)
                curr_date_in_format, curr_time_in_format = timestamp.split()  
                img_dir, img_filename = get_img_path()
                tag_code, curr_msg, media_link = driver.get_tagcode(curr_msg, img_dir, img_filename)
                msg = (group_name, msg_sender, curr_msg, curr_date_in_format, curr_time_in_format, tag_code, media_link)
                driver.write_excel(csv_file_name, msg)
                
except BaseException as error:
    print('An exception occurred: {}'.format(error))
    print('Exiting..')
    driver.graceful_exit()