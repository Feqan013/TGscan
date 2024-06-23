import asyncio
import concurrent.futures
import glob
import json
import re
import shutil
import subprocess
import sys
import threading
import time
import zipfile
import pyzipper
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram import Bot
from telegram.error import RetryAfter, TelegramError
from telegram.request import HTTPXRequest
from TGjsoncreator import process_lines_and_create_json

problemli = []
az_lines=[]
withchannels=[]
weekday_map = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
telegram_bot_token = '6843424140:AAGlHs-JrPPcG1PNXlD_1IrGmcJVwIZpv8E'
telegram_chat_id = '766478351'
chrome_profile_data ='--user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
download_directory = 'C:\\Users\\user\\Downloads\\download_folder'
tgleaks_folder = 'D:\\tgleaks'
telegram_local_storage = 'C:\\Users\\user\\PycharmProjects\\pythonProject\\telegram_local_storage.json'
folder_7zip_exe = "C:\\Program Files\\7-Zip"
def escape_markdown(text):
    # Ensure that the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string")


    #escaped_text = re.sub(r'([_*[\]()~`>#+\|=\\{}.!-])', r'\\\1', text)
    escaped_text = text
    return escaped_text

async def send_message(bot, chat_id, message):
    max_retries = 45
    retries = 0

    while retries < max_retries:
        try:
            escaped_message = escape_markdown(message)
            await bot.send_message(chat_id=chat_id, text=escaped_message)
            break  # Message sent successfully, exit loop
        except RetryAfter as e:
            # Handle flood control, wait for the specified duration
            retry_after = e.retry_after
            print(f"Flood control exceeded. Retrying in {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            retries += 1
        except TelegramError as ex:
            print(f"Error sending message: {ex}")
            break  # Break loop on other exceptions

        if retries == max_retries:
            print("Failed to send message after multiple retries.")
def send_photo(photo_path):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"

    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': telegram_chat_id}

            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            print(f"Photo sent: {photo_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending photo: {e}")



bot = Bot(token=telegram_bot_token, request=HTTPXRequest(connection_pool_size=20))
options = Options()
options.add_argument(chrome_profile_data)
options.add_argument('--profile-directory=Default')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
prefs = {'download.default_directory': download_directory}
options.add_experimental_option('prefs', prefs)
driver = None
def loadtg(options):
    global driver
    driver = webdriver.Chrome(options=options)

    print("Telegram yuklenir")

    print("..........")

    time.sleep(2)
    driver.get('https://web.telegram.org/k')
    time.sleep(2)


    # Load the local storage data from the JSON file
    with open(telegram_local_storage, 'r') as f:
        local_storage = json.load(f)
    time.sleep(3)

    for key, value in local_storage.items():

        script = f"window.localStorage.setItem('{key}', '{value}');"
        try:
            driver.execute_script(script)
        except Exception as e:
            print(f"Error setting local storage item {key}: {e}")


    driver.refresh()
    time.sleep(3)



def keyword_search(kword):
    global driver
    try:
        if not driver:
            loadtg(options)
        time.sleep(5)
        input_element = driver.find_element(By.CSS_SELECTOR, ".input-field-input.input-search-input.is-empty")
        input_element.send_keys(kword)
        print("Axtarilir :",kword)
        time.sleep(2)

        elements = driver.find_elements(By.CSS_SELECTOR,
                                        "a.row.no-wrap.row-with-padding.row-clickable.hover-effect.rp.chatlist-chat.chatlist-chat-bigger.row-big")
        with open('previous_results.txt', 'r', encoding='utf-8') as previous_file:
            previous_results = previous_file.read()
        today_date = datetime.now().strftime("%Y-%m-%d")
        for element in elements:
            try:
                print(element)
                date_text = element.find_element(By.CLASS_NAME, 'message-time').text
                print(date_text)
                if re.match(r'^\d{1,2}:\d{2}$', date_text):
                    element.click()
                    time.sleep(1)
                    person_div = driver.find_element(By.XPATH, '//div[@class="person"]')
                    h3_text_element = person_div.find_element(By.CLASS_NAME, 'peer-title')
                    h3_text = h3_text_element.text.strip()
                    print(h3_text)

                    if "PIN-UP" not in h3_text and h3_text != "F0llow3r__":
                        focused_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "highlighted")]'))
                        )
                        message_element = focused_element.find_element(By.CLASS_NAME, 'translatable-message')
                        message_html = message_element.get_attribute("outerHTML")

                        # Parse the HTML using BeautifulSoup to get the text content
                        soup = BeautifulSoup(message_html, 'html.parser')
                        text_content = soup.get_text()
                        time.sleep(1)

                        if kword == ".az" and ".az" not in text_content:
                            continue
                        chat_info = (
                            f'Keyword : {kword} \nChannel : {h3_text} \nTime : {date_text} \nDate : {today_date} \n{text_content.strip()}\n')
                        print(chat_info)
                        if chat_info not in previous_results:
                            with open('C:\\Users\\user\\PycharmProjects\\pythonProject\\previous_results.txt', 'a', encoding='utf-8') as previous_file:
                                previous_file.write(chat_info)
                                screen_element = driver.find_element(By.CLASS_NAME, 'chat.tabs-tab.active.can-click-date')
                                sanitized_filename = re.sub(r'[\\/:*?"<>|]', '_',
                                                            f"{today_date}_{date_text}_{h3_text}.png")
                                screenshot_path = os.path.join(os.getcwd(), sanitized_filename)
                                try:
                                    screen_element.screenshot(screenshot_path)
                                except e:
                                    print(e)
                                print(f"Screenshot saved as {screenshot_path}")
                                time.sleep(3)
                                send_photo(screenshot_path)
                                asyncio.run(send_message(bot, telegram_chat_id, chat_info))
            except Exception as e:
                print(f"Error processing element: {e}")
                continue

        time.sleep(1)
        input_element = driver.find_element(By.CLASS_NAME, 'input-field-input')
        driver.execute_script("arguments[0].scrollIntoView();", input_element)
        time.sleep(3)
        for _ in range(len(input_element.get_attribute('value'))):
            input_element.send_keys(Keys.BACKSPACE)
    except Exception as e:
        print(f"Error in keyword_search for '{kword}': {e}")

def check_and_send_txt_files(searchfor, start_date):
    global driver
    scroll_count = 0
    loadtg(options)
    time.sleep(4)
    input_element = driver.find_element(By.CSS_SELECTOR, ".input-field-input.input-search-input.is-empty")
    input_element.send_keys(searchfor)
    time.sleep(5)
    elements = driver.find_elements(By.CSS_SELECTOR, "a.row.no-wrap.row-with-padding.row-clickable.hover-effect.rp.chatlist-chat.chatlist-chat-bigger.row-big")

    max_scroll_count = 100
    counter = 1
    if len(start_date) !=3:
        month, day = start_date.split()
        if day == 1:
            day = 30
        day = int(day) - 1
        download_date=f"{month} {day}"
    else:
        yesterday = datetime.now() - timedelta(days=2)
        weekday_num = yesterday.weekday()
        download_date = weekday_map[weekday_num]
        print("2 gun evvel: ",download_date)
    while scroll_count < max_scroll_count:
        elements = driver.find_elements(By.CSS_SELECTOR, "a.row.no-wrap.row-with-padding.row-clickable.hover-effect.rp.chatlist-chat.chatlist-chat-bigger.row-big")
        time.sleep(1)
        print(scroll_count)
        if elements:
            last_element = elements[-1]
            last_element.click()
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView(true);", last_element)
            wait = WebDriverWait(driver, 3)
            wait.until(EC.visibility_of(last_element))
            time.sleep(1)
            download_date_html = f">{download_date}</span>"
            if download_date_html in driver.page_source.lower():
                print(download_date)
                scroll_count += 50
        else:
            break
        counter += 1


    time.sleep(2)
    counter = 1
    download_date = start_date.lower()
    for element in elements:
        date_text = element.find_element(By.CLASS_NAME, 'message-time').text.lower()

        print(date_text)



        print("download date 2: ",download_date)
        if date_text == download_date:
            element.click()
            time.sleep(1)
            try:
                focused_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "highlighted")]'))
                )
                document_ico = focused_element.find_element(By.CLASS_NAME, 'document-ico')
                time.sleep(3)
                document_ico.click()
                time.sleep(3)
                cntr = 0
                while True:
                    if all(indicator not in driver.page_source for indicator in ["downloading"]):
                        time.sleep(1)
                        break
                    time.sleep(2)
                    cntr += 1
                    print("Counter :", cntr)
                    if cntr == 500:
                        break
                driver.execute_script("arguments[0].scrollIntoView();", element)
            except Exception as e:
                print(e)
                cntr = 0
                while True:
                    if all(indicator not in driver.page_source for indicator in ["downloading"]):
                        time.sleep(1)
                        break
                    time.sleep(2)
                    cntr += 1
                    print("Counter :", cntr)
                    if cntr == 500:
                        break
                driver.execute_script("arguments[0].scrollIntoView();", element)
                pass
        time.sleep(0.5)
        counter += 1  # Increment counter for each element

    if searchfor == ".rar":
        remove_duplicate_files(download_directory)
        time.sleep(5)
    else:
        pass
    time.sleep(5)
def extract_zip(zip_path, passwords, success_flag):
    base_dir = f"{download_directory}\\extracted_files"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    filename = os.path.splitext(os.path.basename(zip_path))[0]
    extract_dir = os.path.join(base_dir, filename)
    if ".zip" in zip_path:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f"Extraction successful without password: {zip_path}")
                success_flag.set()
                return

        except Exception as e:
            try:
                with pyzipper.AESZipFile(zip_path, 'r') as zip_ref:
                    print("2")
                    zip_ref.extractall(extract_dir)
                    success_flag.set()
                    return
            except Exception as e:
                for password in passwords:
                    print(password,zip_path)
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            print("3")
                            zip_ref.extractall(extract_dir, pwd=bytes(password, 'utf-8'))
                            print(f"Extraction successful with password: {password}, {zip_path}")
                            success_flag.set()
                            return
                    except Exception as e:
                        try:
                            with pyzipper.AESZipFile(zip_path, 'r') as zip_ref:
                                print("4")
                                zip_ref.extractall(extract_dir, pwd=bytes(password, 'utf-8'))
                                print(f"Extraction successful with password: {password}, {zip_path}")
                                success_flag.set()

                                print(f"Error extracting with password {password}: {e}")
                                return
                        except:
                            pass

            print(e)
    else:
        if passwords:
            for password in passwords:
                try:
                    print(password)
                    subprocess.run([f"{folder_7zip_exe}\\7z.exe", "t", "-p" + password, zip_path], check=True,
                                   capture_output=True)
                    subprocess.run(
                        [f"{folder_7zip_exe}\\7z.exe", "x", "-y", zip_path, "-p" + password, "-o" + extract_dir],
                        check=True,
                        stdin=subprocess.DEVNULL  # Suppress any prompts
                    )

                    print(f"Extraction successful with password: {password}, {zip_path}")
                    success_flag = True
                    return success_flag
                except subprocess.CalledProcessError as e:
                    if "Wrong password" in str(e):
                        print(f"Skipping wrong password: {password}")
                        continue
                    else:
                        print(f"Error extracting with password {password}: {e}")
def read_txt_files():
    global withchannels
    unzip_dir = download_directory
    # Read passwords from the file
    with open(f"{tgleaks_folder}\\tgzip_passwords.txt", 'r', encoding='utf-8') as passwords_file:
        passwords = passwords_file.read().splitlines()
    # List all .zip files
    zip_files = [filename for filename in os.listdir(download_directory) if filename.endswith(".zip") or filename.endswith(".rar")]

    for zip_filename in zip_files:
        print(zip_filename)
        zip_file_path = os.path.join(download_directory, zip_filename)

        if (zip_filename.endswith(".zip") or zip_filename.endswith(".rar")) and "part" not in zip_filename:
            # Use ThreadPoolExecutor for parallel extraction with multiple passwords
            success_flag = threading.Event()  # Event to signal successful extraction
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(extract_zip, zip_file_path, passwords, success_flag)
                # Wait for successful extraction or completion of all password attempts
                executor.shutdown(wait=True)
                if success_flag.is_set():
                    # Successful extraction occurred, stop processing other zip files
                    continue

    for root, dirs, files in os.walk(unzip_dir):
        for unzipped_filename in files:
            unzipped_file_path = os.path.join(root, unzipped_filename)
            if unzipped_filename.endswith(".txt") and "cookie" not in unzipped_file_path.lower() and "domain" not in unzipped_file_path.lower() and "profile" not in unzipped_file_path.lower() and "default" not in unzipped_file_path.lower() and "history" not in unzipped_file_path.lower():
                print(f"fayl : {unzipped_file_path.lower()}")
                # Open and read the unzipped file
                with open(unzipped_file_path, 'r', encoding='utf-8') as file:
                    try:
                        if "passwords" in unzipped_file_path.lower() and (any(re.search(r'\b\w+\.az\b(?![.@])', line) for line in file)):
                            extract_data_and_append(unzipped_file_path)
                        else:
                            for line in file:
                                if re.search(r'\b\w+\.az\b(?![.@])', line) and (":" or "|" or " " in line) and "autofill" not in unzipped_filename.lower() and "grab" not in unzipped_file_path.lower() and ("TRUE" and "FALSE" not in line):
                                    # Check if the line exists in tgleaks.txt before processing it
                                    if not line_exists_in_tgleaks(line):
                                        withchannels.append(f"{unzipped_file_path}\n{line.strip()}\n")
                                        print("setir  ",line)
                                        az_lines.append(f"{line.strip()}")
                                        write_daily(
                                                f"{line.strip()}:{unzipped_filename}")
                                        write_withchannels(unzipped_file_path, line.strip())
                                else:
                                    pass
                    except:
                        pass

def write_daily(line):
    global start_date
    if len(start_date) == 3:
        yesterday = datetime.today() - timedelta(days=1)
        start_date = yesterday.strftime('%b %d')
    with open(f'{tgleaks_folder}\\tgleaks_{start_date}.txt', 'a',
              encoding='utf-8') as leakfile_daily:
        leakfile_daily.write(f"{line}\n")
def write_withchannels(unzipped_file_path,line):
    with open(f'{tgleaks_folder}\\tgleaks.txt', 'a', encoding='utf-8') as leakfile:
        leakfile.write(f"{unzipped_file_path}\n{line.strip()}\n")
def extract_data_and_append(file_path):
    global pattern
    vers=0
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    if "Host" in data:
        pattern = re.compile(r'Soft: (.+)\nHost: (.+)\nLogin: (.*)\nPassword: (.+)', re.MULTILINE)
        vers =1
    elif "Storage" in data:
        pattern = re.compile(r'Storage: (.+)\nURL: (.+)\nLogin: (.*)\nPassword: (.+)', re.MULTILINE)
        vers=2
    elif "Application" in data:
        pattern = re.compile(r'URL: (.+)\nUsername: (.*)\nPassword: (.+)\nApplication: (.+)', re.MULTILINE)
        vers=3
    elif "SOFT" in data:
        pattern = re.compile(r'SOFT: (.+)\nURL: (.*)\nUSER: (.+)\nPASS: (.+)', re.MULTILINE)
        vers=4
    matches = pattern.findall(data)

    for match in matches:
        if ".az" in match[1] or ".az" in match[2] or ".az" in match[0]:
            print("matched")
            if vers == 1:
                print(f"hesab {match[1]}:{match[2]}:{match[3]}")
                if not line_exists_in_tgleaks(f"{match[1]}:{match[2]}:{match[3]}"):
                    az_lines.append(f"{match[1]}:{match[2]}:{match[3]}")
                    withchannels.append(f"{file_path}\n{match[1]}:{match[2]}:{match[3]}\n")
                    write_withchannels(file_path, f"{match[1]}:{match[2]}:{match[3]}")
                    write_daily(
                        f"{match[1]}:{match[2]}:{match[3]}:{file_path.lstrip(f'{download_directory}\\extracted_files\\')}")
            elif vers == 2:
                if not line_exists_in_tgleaks(f"{match[1]}:{match[2]}:{match[3]}"):
                    print(f"hesab {match[1]}:{match[2]}:{match[3]}")
                    az_lines.append(f"{match[1]}:{match[2]}:{match[3]}")
                    withchannels.append(f"{file_path}\n{match[1]}:{match[2]}:{match[3]}\n")
                    write_withchannels(file_path, f"{match[1]}:{match[2]}:{match[3]}\n")
                    write_daily(
                        f"{match[1]}:{match[2]}:{match[3]}:{file_path.lstrip(f'{download_directory}\\extracted_files\\')}")
            elif vers == 3:
                if not line_exists_in_tgleaks(f"{match[0]}:{match[1]}:{match[2]}"):
                    print(f"hesab {match[0]}:{match[1]}:{match[2]}")
                    az_lines.append(f"{match[0]}:{match[1]}:{match[2]}")
                    withchannels.append(f"{file_path}\n{match[0]}:{match[1]}:{match[2]}\n")
                    write_daily(
                        f"{match[0]}:{match[1]}:{match[2]}:{file_path.lstrip(f'{download_directory}\\extracted_files\\')}")
                    write_withchannels(file_path, f"{match[0]}:{match[1]}:{match[2]}")
            elif vers == 4:
                if not line_exists_in_tgleaks(f"{match[1]}:{match[2]}:{match[3]}"):
                    print(f"hesab {match[1]}:{match[2]}:{match[3]}")
                    az_lines.append(f"{match[1]}:{match[2]}:{match[3]}")
                    withchannels.append(f"{file_path}\n{match[1]}:{match[2]}:{match[3]}\n")
                    write_daily(
                        f"{match[1]}:{match[2]}:{match[3]}:{file_path.lstrip(f'{download_directory}\\extracted_files\\')}")
                    write_withchannels(file_path, f"{match[1]}:{match[2]}:{match[3]}")
        else:
            pass


def line_exists_in_tgleaks(line):
    # Check if the line exists in tgleaks.txt
    tgleaks_path = f'{tgleaks_folder}\\tgleaks.txt'
    with open(tgleaks_path, 'r', encoding='utf-8') as tgleaks_file:
        fayl = tgleaks_file.read()
        setirler = tgleaks_file.readlines()

        if line.strip() in fayl:
            pass

        for existing_line in tgleaks_file:
            if line.strip() == existing_line.strip():
                pass

        for existing_line in setirler:
            if line.strip() == existing_line.strip():
                pass

    return False
def deduplicate_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = set(lines)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)


def remove_all():
    directory_path = download_directory

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File '{filename}' deleted successfully.")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Directory '{filename}' deleted successfully.")
        except FileNotFoundError:  # Catch specific error for missing file
            print(f"File '{filename}' not found. Skipping...")
            continue
        except PermissionError as e:  # Catch permission issues
            print(f"Error deleting '{filename}': Permission denied ({e})")
        except Exception as e:  # Catch other unexpected errors
            print(f"Unexpected error deleting '{filename}': {e}")



def remove_all_system():
    directory_path = f"{download_directory}\\extracted_files"

    # Use subprocess to call system commands for file and directory removal
    for filename in glob.glob(os.path.join(directory_path, "*")):
        file_path = os.path.join(directory_path, filename)
        print(file_path)
        print(os.listdir(directory_path))
        try:
            if os.path.isfile(file_path):
                # Use system command 'del' to remove files
                subprocess.run(['del', file_path], check=True, shell=True)
                print(f"File '{filename}' deleted successfully.")
            elif os.path.isdir(file_path):
                print("folder")
                # Use system command 'rmdir' to remove directories
                subprocess.run(['rmdir', '/S', '/Q', file_path], check=True, shell=True)
                print(f"Directory '{filename}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting '{filename}': {e}")
            continue


import os
import hashlib

def remove_duplicate_files(root_dir):
    """Remove duplicate files in the given directory."""
    # Dictionary to store files by their hashes
    files_by_hash = {}
    # List to store duplicate files
    duplicates = []

    def file_hash(file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # 64 KB chunks
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    # Traverse the directory
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Calculate the hash of the file
            file_hash_value = file_hash(file_path)
            # Add the file to the dictionary
            files_by_hash.setdefault(file_hash_value, []).append(file_path)

    # Check for duplicates
    for file_list in files_by_hash.values():
        if len(file_list) > 1:
            duplicates.extend(file_list[1:])

    # Remove duplicate files
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Removed duplicate: {duplicate}")

def main():
    try:
        keywords = None
        global counter
        global start_date

        if '-k' in sys.argv:
            k_index = sys.argv.index('-k')
            keywords = sys.argv[k_index + 1:]
            print("Axtarilir: ",keywords)
        elif len(sys.argv) != 2:
            # Calculate yesterday's date
            yesterday = datetime.now() - timedelta(days=1)
            # Get the weekday number of yesterday (0 = Monday, 6 = Sunday)
            weekday_num = yesterday.weekday()
            # Get the weekday abbreviation from the map
            start_date = weekday_map[weekday_num]
        else:
            start_date = sys.argv[1]




        try:
            ascii_art = """
        d888888b  d888b  .d8888.  .o88b.  .d8b.  d8b   db 
        `~~88~~' 88' Y8b 88'  YP d8P  Y8 d8' `8b 888o  88 
           88    88      `8bo.   8P      88ooo88 88V8o 88 
           88    88  ooo   `Y8b. 8b      88~~~88 88 V8o88 
           88    88. ~8~ db   8D Y8b  d8 88   88 88  V888 
           YP     Y888P  `8888Y'  `Y88P' YP   YP VP   V8P 

            t.me/Feqan13
            """

            print(ascii_art)

            if keywords:
                while True:
                    for keyword in keywords:
                        keyword_search(keyword)

                    time.sleep(30)  # Wait for 5 minutes before checking again
            with open(f'{tgleaks_folder}\\tgleaks.txt', 'a', encoding='utf-8') as leakfile:
                pass

            file_path = f'{tgleaks_folder}\\tgleaks_{start_date}.txt'
            if not os.path.exists(file_path):
                with open(file_path, 'a', encoding='utf-8') as leakfile_daily:
                    pass

            #check_and_send_txt_files(".txt", start_date)
            #driver.quit()
            #check_and_send_txt_files(".zip", start_date)
            #driver.quit()
            #check_and_send_txt_files(".rar", start_date)
            #driver.quit()
            time.sleep(2)
            read_txt_files()
            time.sleep(12)
            deduplicate_lines(f'{tgleaks_folder}\\tgleaks_{start_date}.txt')
            time.sleep(5)
            if len(start_date) == 3:
                yesterday = datetime.today() - timedelta(days=1)
                start_date = yesterday.strftime('%b %d')
            process_lines_and_create_json(
                f'{tgleaks_folder}\\tgleaks_{start_date}.txt',
                f'{tgleaks_folder}\\tgleak_{start_date}.json', start_date)
            time.sleep(10)
            try:
                remove_all_system()
                remove_all()
            except Exception as e:
                print(e)
                try:
                    remove_all_system()
                except Exception as e:
                    print(e)
                    pass
        except Exception as e:
            print(e)
            pass

        if keywords:
            while True:
                for keyword in keywords:
                    keyword_search(keyword)
                time.sleep(300)

    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()
