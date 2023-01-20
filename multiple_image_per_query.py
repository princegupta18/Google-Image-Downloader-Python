import time
import base64
from io import BytesIO
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

cwd = os.getcwd()
IMAGE_FOLDER = 'electricityBill'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 1

def download_google_images(search_query: str, number_of_images: int) -> str:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''

    def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(SLEEP_TIME)

            new_height = driver.execute_script('return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(SLEEP_TIME)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="//input[contains(@class,'gLFyf')]"
    )

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    scroll_to_bottom()
    time.sleep(SLEEP_TIME)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
    )

    total_images = len(img_results)

    print(f'Total images - {total_images}')

    count = 0

    for img_result in img_results:
        try:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            img_result.click()
            time.sleep(SLEEP_TIME)

            actual_imgs = driver.find_elements(
                by=By.XPATH,
                value="//img[contains(@class,'n3VNCb')]"
            )

            src = ''

            for actual_img in actual_imgs:
                if 'https://encrypted' in actual_img.get_attribute('src'):
                    pass
                elif 'http' in actual_img.get_attribute('src'):
                    src += actual_img.get_attribute('src')
                    break
                else:
                    pass

            for actual_img in actual_imgs:
                if src == '' and 'base' in actual_img.get_attribute('src'):
                    src += actual_img.get_attribute('src')

            if 'https://' in src:
                image_name = search_query.replace('/', ' ')
                image_name = re.sub(pattern=" ", repl="_", string=image_name)
                file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
                try:
                    result = requests.get(src, allow_redirects=True, timeout=10)
                    open(file_path, 'wb').write(result.content)
                    img = Image.open(file_path)
                    img = img.convert('RGB')
                    img.save(file_path, 'JPEG')
                    print(f'Count - {count} - Image saved from https.')
                except:
                    print('Bad image.')
                    try:
                        os.unlink(file_path)
                    except:
                        pass
                    count -= 1
            else:
                img_data = src.split(',')
                image_name = search_query.replace('/', ' ')
                image_name = re.sub(pattern=" ", repl="_", string=image_name)
                file_path = f'{IMAGE_FOLDER}/{count}_{image_name}.jpeg'
                try:
                    img = Image.open(BytesIO(base64.b64decode(img_data[1])))
                    img = img.convert('RGB')
                    img.save(file_path, 'JPEG')
                    print(f'Count - {count} - Image saved from Base64.')
                except:
                    print('Bad image.')
                    count -= 1
        except ElementClickInterceptedException as e:
            count -= 1
            print(e)
            print('Image is not clickable.')
            driver.quit()

        count += 1

        if count >= total_images:
            print('No more images to download.')
            break
        if count == number_of_images:
            break

tags = [
    'Real Indian Electricity Bill'
    'Electricity Bill of Central Electricity Authority',
    'Electricity Bill of Central Electricity Regulatory Commission',
    'Electricity Bill of Bureau of Energy Efficiency',
    'Electricity Bill of Nuclear Power Corporation of India',
    'Electricity Bill of PowerGrid Corporation of India',
    'Electricity Bill of NHPC Limited',
    'Electricity Bill of NTPC Limited',
    'Electricity Bill of Power System Operation Corporation',
    'Electricity Bill of Neyveli Lignite Corporation',
    'Electricity Bill of Damodar Valley Corporation',
    'Electricity Bill of Andhra Pradesh Power Generation Corporation',
    'Electricity Bill of Transmission Corporation of Andhra Pradesh',
    'Electricity Bill of Andhra Pradesh Eastern Power Distribution Company Limited',
    'Electricity Bill of Andhra Pradesh Central Power Distribution Company Limited',
    'Electricity Bill of Andhra Pradesh Southern Power Distribution Company Limited',
    'Electricity Bill of Assam State Electricity Board',
    'Electricity Bill of Bihar State Power Holding Company Limited',
    'Electricity Bill of North Bihar Power Distribution Company Limited',
    'Electricity Bill of South Bihar Power Distribution Company Limited',
    'Electricity Bill of Chhattisgarh State Power Generation Company Limited',
    'Electricity Bill of Dakshin Gujarat Vij Company Ltd.',
    'Electricity Bill of Gujarat Urja Vikas Nigam Ltd.',
    'Electricity Bill of Madhya Gujarat Vij Company Ltd.',
    'Electricity Bill of Paschim Gujarat Vij Company Ltd.',
    'Electricity Bill of Gujarat State Electricity Corporation Ltd.',
    'Electricity Bill of Gujarat Electricity Corporation Ltd.',
    'Electricity Bill of Uttar Gujarat Vij Company Ltd.',
    'Electricity Bill of Dakshin Haryana Bijli Vitran Nigam',
    'Electricity Bill of Uttar Haryana Bijli Vitran Nigam',
    'Electricity Bill of Haryana Vidyut Prasaran Nigam Limited',
    'Electricity Bill of Haryana Power Generation Corporation',
    'Electricity Bill of Delhi Vidyut Board',
    'Electricity Bill of Delhi Electricity Regulatory Commission',
    'Electricity Bill of Delhi Transco Limited',
    'Electricity Bill of BRPL',
    'Electricity Bill of BYPL',
    'Electricity Bill of TPDDL',
    'Electricity Bill of IPGCL',
    'Electricity Bill of PPCL',
    'Electricity Bill of Jharkhand State Electricity Board',
    'Electricity Bill of Karnataka Power Corporation Limited (KPCL)',
    'Electricity Bill of Karnataka Power Transmission Corporation Limited (KPTCL)',
    'Electricity Bill of MESCOM, Mangaluru',
    'Electricity Bill of CESC, Mysuru',
    'Electricity Bill of BESCOM, Bengaluru',
    'Electricity Bill of HESCOM, Hubballi',
    'Electricity Bill of GESCOM, Kalaburagi',
    'Electricity Bill of Kerala State Electricity Board',
    'Electricity Bill of Madhya Pradesh Power Generation Company Limited',
    'Electricity Bill of Madhya Pradesh Power Transmission Company Limited',
    'Electricity Bill of Madhya Pradesh Poorv Kshetra Vidyut Company Limited',
    'Electricity Bill of Madhya Pradesh Madhya Kshetra Vidyut Vitaran Company Limited',
    'Electricity Bill of Madhya Pradesh Paschim Kshetra Vidyut Vitaran Company Limited',
    'Electricity Bill of Madhya Pradesh Power Management Company Limited',
    'Electricity Bill of Madhya Pradesh Electricity Regulatory Commission',
    'Electricity Bill of Maharashtra State Electricity Board',
    'Electricity Bill of Maharashtra State Electricity Distribution Company Limited',
    'Electricity Bill of Maharashtra State Electricity Transmission Company Limited',
    'Electricity Bill of Maharashtra State Power Generation Company Limited',
    'Electricity Bill of Rajasthan Rajya Vidyut Utpadan Nigam',
    'Electricity Bill of Rajasthan Rajya Vidyut Prasaran Nigam Limited',
    'Electricity Bill of Uttar Pradesh Rajya Vidyut Utpadan Nigam (UPRVUN)',
    'Electricity Bill of Uttar Pradesh Rajya Vidyut Utpadan Nigam Limited (UPRVUNL)',
    'Electricity Bill of Uttar Pradesh Power Corporation Limited (UPPCL)',
    'Electricity Bill of UP Power Transmission Corporation Limited (UPPTCL)',
    'Electricity Bill of UP Jal Vidyut Nigam Limited (UPJVNL)',
    'Electricity Bill of West Bengal Power Development Corporation Limited',
    'Electricity Bill of West Bengal State Electricity Board',
    'Electricity Bill of CESC',
    'Electricity Bill of Odisha Hydro Power Corporation',
    'Electricity Bill of Odisha Power Generation Corporation',
    'Electricity Bill of Odisha Electricity Regulatory Commission',
    'Electricity Bill of Central Electricity Supply Utility of Odisha',
    'Electricity Bill of Western Electricity Supply Company of Odisha',
    'Electricity Bill of Odisha Power Transmission Corporation Limited',
    'Electricity Bill of TP Northern Odisha Distribution Limited (TPNODL)',
    'Electricity Bill of TNEB Limited',
    'Electricity Bill of Tamil Nadu Generation and Distribution Corporation Limited',
    'Electricity Bill of Tamil Nadu Transmission Corporation Limited',
    'Electricity Bill of Tamil Nadu Energy Development Agency',
    'Electricity Bill of Tamil Nadu Electrical Licensing Board',
    'Electricity Bill of Tamil Nadu Electricity Regulatory Commission',
    'Electricity Bill of Tamil Nadu Electrical Inspectorate',
    'Electricity Bill of Telangana Power Generation Corporation',
    'Electricity Bill of Transmission Corporation of Telangana',
    'Electricity Bill of Telangana State Northern Power Distribution Company Limited',
    'Electricity Bill of Telangana State Southern Power Distribution Company Limited',
    'Electricity Bill of Punjab State Power Corporation Limited',
    'Electricity Bill of Punjab State Power Transmission Corporation Limit'


]

for tag in tags:
    print(f'{"="*10} Downloding for the tag - {tag} {"="*10}')
    download_google_images(
        tag,
        3
    )
    print(f'{"="*10} Finished downloding for the tag - {tag} {"="*10}')

driver.quit()
