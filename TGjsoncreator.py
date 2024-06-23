import json
from datetime import datetime, timedelta
#from confluent_kafka import Producer, KafkaError

tgleaks_folder = 'D:\\tgleaks'

# conduktor.io ve apache kafka islenerse
"""kafka_broker = 'kafka0:9092'
# Define the Kafka producer configuration
producer_config = {
    "bootstrap.servers": "10.10.22.24:9092",
    'acks':'all',
    'enable.idempotence': True,  # Enable idempotence
    'compression.type': 'snappy',  # Compression type (e.g., 'gzip')
    'batch.size':16384
}

topic="telegram_data
producer = Producer(producer_config)"""
data = []
data_notparsed = []
def process_lines_and_create_json(file_path, json_output_path,date):
    if len(date) == 3:
        yesterday = datetime.today() - timedelta(days=1)
        date = yesterday.strftime('%b %d')
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                print(line)
                parts = line.strip().split(':')
                if len(parts) == 6:
                    print("5555", line)
                    if 'http' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0]+parts[1]+parts[2], 'Username': parts[3], 'Password': parts[4], 'Date': date, 'File': parts[-1]})
                    elif '.az' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0]+parts[1]+parts[2], 'Username': parts[3], 'Password': parts[4], 'Date': date, 'File': parts[-1]})
                    if '.com' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0]+parts[1]+parts[2], 'Username': parts[3], 'Password': parts[4], 'Date': date, 'File': parts[-1]})
                    elif 'http' in parts[2]:
                        # If http is in the end, URL is the first part, and the rest is Username:Password
                        data.append({'URL': parts[2]+parts[3]+parts[4], 'Username': parts[0], 'Password':parts[1], 'Date': date, 'File': parts[-1]})
                elif len(parts) == 5:
                    if 'http' in parts[0]:
                        print("partssssss ----", line)
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0]+parts[1], 'Username': parts[2], 'Password': parts[3], 'Date': date, 'File': parts[-1]})
                    elif 'http' in parts[2]:
                        print("partsssz ----", line)
                        # If http is in the end, URL is the first part, and the rest is Username:Password
                        data.append({'URL': parts[2]+parts[3], 'Username': parts[0], 'Password':parts[1], 'Date': date, 'File': parts[-1]})
                elif len(parts) == 4 and " " in parts[-1]:
                    print("5555", line)
                    if 'http' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0]+parts[1]+parts[2], 'Username': parts[3], 'Password': parts[4], 'Date': date, 'File': parts[-1]})
                    elif '.az' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0], 'Username': parts[1], 'Password': parts[2], 'Date': date, 'File': parts[-1]})
                    elif '.az' in parts[1]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0], 'Username': parts[1], 'Password': parts[2],
                                     'Date': date, 'File': parts[-1]})
                    elif 'http' in parts[2]:
                        # If http is in the end, URL is the first part, and the rest is Username:Password
                        data.append({'URL': parts[2]+parts[3]+parts[4], 'Username': parts[0], 'Password':parts[1], 'Date': date, 'File': parts[-1]})
                elif len(parts) == 4 and " " not in line:
                    if '.az' in parts[0]:
                        # If http is in the beginning, URL is the second part, and the rest is Username:Password
                        data.append({'URL': parts[0], 'Username': parts[1], 'Password': parts[2], 'Date': date, 'File': parts[-1]})
                    elif '.az' in parts[2]:
                        # If http is in the end, URL is the first part, and the rest is Username:Password
                        data.append({'URL': parts[2], 'Username': parts[0], 'Password':parts[1], 'Date': date, 'File': parts[-1]})
                    else:
                        print("hhhhhhhhhhhhh ",line)
                        data_notparsed.append({'URL': line, 'Username': "NOTPARSED", 'Password': "NOTPARSED",
                                               'Date': date, 'File': parts[-1]})
                        # Otherwise, assume the first part is Username, and the rest is Password
                        data.append({'Username': parts[0], 'Password': ':'.join(parts[1:]), 'Date': date, 'File': parts[-1]})
                elif " " in line:
                    url, credentials = line.split(' ', 1)
                    username, password_and_file = credentials.split(':', 1)
                    password_parts = password_and_file.rsplit(':', 1)
                    if len(password_parts) == 2:
                        password, file_part = password_parts
                    else:
                        password = password_parts[0]
                        file_part = ""
                    data.append({
                        'URL': url,
                        'Username': username,
                        'Password': password,
                        'Date': date,
                        'File': file_part
                    })
                elif len(parts)==3 and "|" not in line:
                        if '@' in parts[0]:
                            # If http is in the beginning, URL is the second part, and the rest is Username:Password
                            data.append({'URL': "MAIL", 'Username': parts[0], 'Password': parts[1], 'Date': date, 'File': parts[-1]})
                        elif '@' in parts[1]:
                            # Otherwise, assume the first part is Username, and the rest is Password
                            data.append({'URL': "MAIL", 'Username': parts[1], 'Password': parts[0], 'Date': date, 'File': parts[-1]})
                elif "|" in line:
                    parts = line.strip().split('|')
                    if 'http' in parts[0]:
                        data.append({
                            'URL': parts[0],
                            'Username': parts[1],
                            'Password': parts[2].split(':')[0],
                            'Date': date,
                            'File': parts[2].split(':')[1]
                        })
                    else:
                        data_notparsed.append({
                            'URL': line,
                            'Username': "NOTPARSED",
                            'Password': "NOTPARSED",
                            'Date': date,
                            'File': parts[-1]
                        })

                elif ".az" in parts[0]:
                    # If http is in the beginning, URL is the second part, and the rest is Username:Password
                    data.append({'URL': parts[0], 'Username': parts[1], 'Password': parts[2], 'Date': date, 'File': parts[-1]})
                elif ".az" in parts[2]:
                    # If http is in the beginning, URL is the second part, and the rest is Username:Password
                    data.append({'URL': parts[2], 'Username': parts[0], 'Password': parts[1],
                                 'Date': date, 'File': parts[-1]})
                elif ".com" in parts[0]:
                    # If http is in the beginning, URL is the second part, and the rest is Username:Password
                    data.append({'URL': parts[0], 'Username': parts[1], 'Password': parts[2], 'Date': date, 'File': parts[-1]})
                elif ".com" in parts[2]:
                    # If http is in the beginning, URL is the second part, and the rest is Username:Password
                    data.append({'URL': parts[2], 'Username': parts[0], 'Password': parts[1],
                                 'Date': date, 'File': parts[-1]})
                else:
                    print(line)
                    data_notparsed.append({'URL': line, 'Username': "NOTPARSED", 'Password': "NOTPARSED",
                                           'Date': date, 'File': parts[-1]})
            except Exception as e:
                print(e)
                pass
        with open(json_output_path, 'a', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
            print(f"Total accounts parsed and saved: {len(data)}")

        new_accounts = []

        def search_in_tgleaks(url, username, password):
            with open(f'{tgleaks_folder}\\tgleaks.json', 'r', encoding='utf-8') as tgleaks_file:
                tgleaks_lines = tgleaks_file.readlines()

                for i in range(len(tgleaks_lines) - 2):
                    if (f'"URL": "{url}"' in tgleaks_lines[i].strip() and
                            f'"Username": "{username}"' in tgleaks_lines[i + 1].strip() and
                            f'"Password": "{password}"' in tgleaks_lines[i + 2].strip()):
                        return True
            return False

        for account in data:
            url = account['URL']
            username = account['Username']
            password = account['Password']
            if not search_in_tgleaks(url, username, password):
                print(url,username,password)
                new_accounts.append(account)

        if new_accounts:
            with open(f'{tgleaks_folder}\\tgleak_{date}_new.json', 'a', encoding='utf-8') as new_file:
                json.dump(new_accounts, new_file, indent=2)
                print(f"New accounts found and saved to new.json: {len(new_accounts)}")

        with open(f'{tgleaks_folder}\\tgleaks.json', 'a', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)


"""process_lines_and_create_json(
    f'D:\\tgleaks\\tgleaks_fri.txt',
    f'D:\\tgleaks\\tgleak_fri.json', "old")"""

"""for item in data:
        value = json.dumps(item, indent=2)
        producer.produce(topic, key=date, value=value)
        producer.poll(0)  # Ensure timely delivery before next message
    #producer.flush()
    topic2 = "telegram_data_NOTPARSED"
    for item in data_notparsed:
        value = json.dumps(item, indent=2)
        producer.produce(topic2, key=date, value=value)
        producer.poll(0)  # Ensure timely delivery before next message
    producer.flush()"""



