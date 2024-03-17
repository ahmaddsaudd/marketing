# ||||||||||||||||||||||||||||||------------Start Imports------------||||||||||||||||||||||||||||||
import pandas as pd
from datetime import datetime
from selenium import webdriver
import time, math, sys, os, subprocess, json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from .models import BackgroundTasks,Response
import datetime
from time import sleep
import os

current_date = datetime.date.today()



# ||||||||||||||||||||||||||||||------------End Imports------------||||||||||||||||||||||||||||||
def addResultsToDB(task_id, findings, keyword, domain,cursor,industry):
    
    #use models 
    try:   
        for finding in findings:
            print(finding)
            print(finding["name"])
            findingString = json.dumps(finding)

            insert_query = (
                "INSERT INTO response (`background_task_id`, `keyword`, `response_object`, `domain_name`, `name`, `designation`, `email`,`industry`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
            )
            insert_values = (
                task_id,
                keyword,
                findingString,
                domain,
                finding['name'],
                finding['designation'],
                finding['email'],
                industry,
            )
            print("BELOW ARE THE INSERT VALUES")
            print(insert_values)

            cursor.execute(insert_query, insert_values)
        conn.commit()
        print("Findings added successfully")
    except Exception as e:
        print("An error occurred while adding findings to DB")
        print(f"Error: {e}")
        conn.rollback()
    cursor.close()


def update_status(task_id, status, cursor):
    try:
        update_query = (
            f"UPDATE background_tasks SET state = '{status}' WHERE id = {task_id}"
        )
        cursor.execute(update_query)
        print(f"Status updated successfully to {status}")
        conn.commit()

    except Exception as e:
        print("We are failing here in update status")
        print(f"Error: {e}")
        conn.rollback()



def printLogs(log):
    now = datetime.date.today()
    filename = "logs.txt"
    content_to_append = f"{now.strftime('%d-%m-%Y||%H:%M:%S')}------{log}\n"

    with open(filename, "a+") as file:
        file.seek(0, 2)
        if file.tell() == 0:
            file.write("\n")
        file.write(content_to_append)

def check_top_tasks_not_processing(cursor):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
            "SELECT * FROM background_tasks WHERE state='processing' ORDER BY id LIMIT 5"
        )
    processing_results = cursor.fetchall()
    cursor.closeIO
    return len(processing_results) == 0
# ||||||||||||||||||||||||||||||------------Argument Handling Start------------||||||||||||||||||||||||||||||
# args = len(sys.argv) - 1
# if(args < 2):
#     sys.exit(f"Domain name missing.\nEg. python {sys.argv[0]} [domain.com] [JD-Keyword] [queue-id]")
# ||||||||||||||||||||||||||||||------------Argument Handling End------------||||||||||||||||||||||||||||||

# ||||||||||||||||||||||||||||||------------Start of Initialization------------||||||||||||||||||||||||||||||
tbody = []
found = {}



# while True:
#     if check_top_tasks_not_processing(cursor):
#         cursor.execute("SELECT * FROM background_tasks WHERE state='pending' ORDER BY id LIMIT 1")
#         result = cursor.fetchone()
#         if result is not None:
#             task_id = result[0]
#             domain = result[1]
#             keyword = result[2]
#             update_status(task_id,'processing')
#             print(task_id,domain,keyword)
#         else: 
#             exit()
#     else:
#         break

###NEED TO SETUP A LOOP FOR WHEN WE HAVE A BATCH ID(BUT THIS WILL RESULT IN 1 BY 1) AND WHEN WE HAVE SINGLE THAT LOOP WILL ONLY RUN ONCE
def custom_condition():
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM background_tasks WHERE state ='processing' AND date=%s LIMIT 3",(current_date,))
        results = cursor.fetchall()
        #print(len(results))

        #print(results)
    except Exception as e:
        print(e)
    if len(results) <= 2:
        return True
    else: 
        return False

if custom_condition():
    print("EXECUTION POSSIBLE")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM background_tasks WHERE state='pending' ORDER BY id LIMIT 1"
    )
    result = cursor.fetchone()
    if result is not None:
        print(result)
        task_id = result['id']
        domain = result['domain_name']
        keyword = result['keyword']
        update_status(task_id, "processing",cursor)

        print(task_id, domain, keyword)
    else:
        exit()

else:
    print("Queue full") 
    exit()

# # Find the first entry with status 'pending'
# cursor.execute(
#     "SELECT * FROM background_tasks WHERE state='pending' ORDER BY id LIMIT 1"
# )
# result = cursor.fetchone()
# if result is not None:
#     print(result)
#     #     # If there is a record with status 'pending', update its status to 'processing'
#     task_id = result['id']
#     domain = result['domain_name']
#     keyword = result['keyword']
#     update_status(task_id, "processing",cursor)

#     print(task_id, domain, keyword)
# else:
#     exit()



# cursor.execute("SELECT * FROM background_tasks WHERE state='pending' ")



queue_id = task_id
checks = [check.strip() for check in keyword.split(",")]
related_words = ["CEO", "ceo", "Ceo", "Founder","founder","Owner", "chief executive officer","Director","Chief Executive Officer","owner"]

for word in checks:
    if word in related_words:
        checks.extend(related_words)
        break

checks = list(set(checks))

print(checks)
# domain = sys.argv[1]
base_url = "https://app.apollo.io"
cold_comapany = False
column_checks = ["Quick Actions"]
chrome_options = Options()
search_result_section_id = 1
company_index = 2
findings = []
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
hostname = "marketing.3plheroes.com:5000"
url = f"{hostname}/resource"
industry = ""

headers = {"Content-Type": "application/json"}
data = {"key": "value"}
cookies = [
    {
        "domain": "app.apollo.io",
        "expiry": 1708342349,
        "httpOnly": False,
        "name": "_dd_s",
        "path": "/",
        "sameSite": "Strict",
        "secure": False,
        "value": "rum=0&expire=1708342346842",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1708946249,
        "httpOnly": False,
        "name": "intercom-session-dyws6i9m",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "YUZObFRobDNqMGRPSVVCazNINHNuMno5bi9nMEJ2MmV2Q2daSkN3Q1REZVVoaTF0UUNWWDFOREE5cXBXRFg3RC0tUlVPa1k2TnczR3VqS1hPNjVJMjlYQT09--5a88344fdec6c44bb8315735f627cda944a3d89b",
    },
    {
        "domain": ".app.apollo.io",
        "expiry": 1708343248,
        "httpOnly": False,
        "name": "__stripe_sid",
        "path": "/",
        "sameSite": "Strict",
        "secure": True,
        "value": "0ca62572-2619-460d-a82b-93771e5eee70ae57d3",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1731671449,
        "httpOnly": False,
        "name": "intercom-device-id-dyws6i9m",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "4ccca0eb-d55b-4d9f-85c9-0ebfb75b93aa",
    },
    {
        "domain": "app.apollo.io",
        "httpOnly": True,
        "name": "_leadgenie_session",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "a5nDg0f1VkmOQYzspI3wsJXzzYEt878Izu8hjXW0oJnBcSdiRjieT9R5M9FduM3TW5bjwQ%2BxUr72kvLsysGczdd1d3NW0LF5lXo2oxCTs%2B9725%2BzxaBCSFe0YgUCRN8uDigmK3ElvCBP7DcaheOQq%2F2MiJz%2BvksYkFWLK5Ir%2BHFxTT0lZ76MH0VgCsYyItHpS%2Ft7hiydY9NCsmBC1R0XDNnj%2B2EobIteq2REqExMaJZf8O6IplDrTzXY3GEhs0UuZwcdeMZTuzaR1YYToVBpME06kSPtPvzbgxQ%3D--Rv4vm7wsI0jm7Oao--hUOvFJ%2FSDKBd2inF56wVxw%3D%3D",
    },
    {
        "domain": "app.apollo.io",
        "httpOnly": False,
        "name": "X-CSRF-TOKEN",
        "path": "/",
        "sameSite": "Lax",
        "secure": True,
        "value": "43Fz1j4WAOm-JZlj8sa6wvgOZiy6cr-egXCKJ2oFQFfKZVdIJn6bBjy3UHlueGlNTcMsjETICxJzG24-feAjhg",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1710847046,
        "httpOnly": False,
        "name": "remember_token_leadgenie_v2",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTFOelprWm1Jd05UTXhOR00zTURKaE9HWTVOR1ZtWWw5c1pXRmtaMlZ1YVdWamIyOXJhV1ZvWVhOb0lnPT0iLCJleHAiOiIyMDI0LTAzLTE5VDExOjE3OjI2LjMxMFoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdG9rZW5fbGVhZGdlbmllX3YyIn19--104ccbbaa22fb5a187dc3bfbd062688dccfe12de",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1739877446,
        "httpOnly": False,
        "name": "_cioid",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "6576dfb05314c702a8f94efb",
    },
    {
        "domain": ".apollo.io",
        "httpOnly": False,
        "name": "ZP_Pricing_Split_Test_Variant",
        "path": "/",
        "sameSite": "Lax",
        "secure": True,
        "value": "23Q4_EC_Z59",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1708343245,
        "httpOnly": False,
        "name": "__hssc",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "21978340.1.1708341445220",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1739877445,
        "httpOnly": False,
        "name": "_cioanonid",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "bcf20e45-253a-8d9c-26de-ce059c82878c",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1742901446,
        "httpOnly": False,
        "name": "amplitude_id_122a93c7d9753d2fe678deffe8fac4cfapollo.io",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "eyJkZXZpY2VJZCI6IjQxNmE2YmEyLTgzNDgtNDE5Zi04YmIxLTNjMDM2YjUxZjFlYVIiLCJ1c2VySWQiOiI2NTc2ZGZiMDUzMTRjNzAyYThmOTRlZmIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE3MDgzNDE0NDQ2NDcsImxhc3RFdmVudFRpbWUiOjE3MDgzNDE0NDY5NzUsImV2ZW50SWQiOjMsImlkZW50aWZ5SWQiOjMsInNlcXVlbmNlTnVtYmVyIjo2fQ==",
    },
    {
        "domain": "app.apollo.io",
        "expiry": 1708342043,
        "httpOnly": True,
        "name": "GCLB",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "CP_moPaCmuC7YA",
    },
    {
        "domain": ".apollo.io",
        "httpOnly": False,
        "name": "__hssrc",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "1",
    },
    {
        "domain": ".app.apollo.io",
        "expiry": 1739877448,
        "httpOnly": False,
        "name": "__stripe_mid",
        "path": "/",
        "sameSite": "Strict",
        "secure": True,
        "value": "e4a4ad2e-0c69-4e7d-b923-e92e98b5691a6d05c2",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1723893445,
        "httpOnly": False,
        "name": "hubspotutk",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "2726f0f80c122614ca7349f408d62674",
    },
    {
        "domain": ".apollo.io",
        "expiry": 1723893445,
        "httpOnly": False,
        "name": "__hstc",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "value": "21978340.2726f0f80c122614ca7349f408d62674.1708341445220.1708341445220.1708341445220.1",
    },
]
# cookies = [{'domain': '.apollo.io', 'expiry': 1706100023, 'httpOnly': False, 'name': 'intercom-session-dyws6i9m', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'UG5GSjRXTHdzaWo3YXp6Nm1RcG1oOVN5Y0plcCszYk9aMGkxSFN1Ulp3Q04xVVB1TVh4R1M0ZURSUG13cnZ0dS0tTUdWWmRXV0xySkFwR1ZLSkxnZndrQT09--85950a3dd9875dbbd240b08ff64c8044941311a8'}, {'domain': 'app.apollo.io', 'expiry': 1705496123, 'httpOnly': False, 'name': '_dd_s', 'path': '/', 'sameSite': 'Strict', 'secure': False, 'value': 'rum=0&expire=1705496120512'}, {'domain': '.apollo.io', 'expiry': 1740055221, 'httpOnly': False, 'name': 'amplitude_id_122a93c7d9753d2fe678deffe8fac4cfapollo.io', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eyJkZXZpY2VJZCI6IjIzMDNkNTJiLTU5ZjYtNDFkNy04NWJmLWYwZTJkNDUxNjZmNFIiLCJ1c2VySWQiOiI2NTc2ZGZiMDUzMTRjNzAyYThmOTRlZmIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE3MDU0OTUyMTczMTEsImxhc3RFdmVudFRpbWUiOjE3MDU0OTUyMjE4NTksImV2ZW50SWQiOjIsImlkZW50aWZ5SWQiOjMsInNlcXVlbmNlTnVtYmVyIjo1fQ=='}, {'domain': '.apollo.io', 'expiry': 1737031221, 'httpOnly': False, 'name': '_cioid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '6576dfb05314c702a8f94efb'}, {'domain': '.apollo.io', 'expiry': 1721047218, 'httpOnly': False, 'name': 'hubspotutk', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'c85064c479299d1e40a400ac39c9588b'}, {'domain': 'app.apollo.io', 'expiry': 1705495815, 'httpOnly': True, 'name': 'GCLB', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'CMSossOs35Hs0QE'}, {'domain': '.apollo.io', 'expiry': 1708173620, 'httpOnly': False, 'name': 'remember_token_leadgenie_v2', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTFOelprWm1Jd05UTXhOR00zTURKaE9HWTVOR1ZtWWw5c1pXRmtaMlZ1YVdWamIyOXJhV1ZvWVhOb0lnPT0iLCJleHAiOiIyMDI0LTAyLTE3VDEyOjQwOjIwLjA2MloiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdG9rZW5fbGVhZGdlbmllX3YyIn19--ce3af59db63aaec57c5dbe6616cd64bd6a300da5'}, {'domain': 'app.apollo.io', 'httpOnly': False, 'name': 'X-CSRF-TOKEN', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'CU1LQsmLn9qg6uj8V7u7H5RKerKcT8CLjbQRiO_UDbb13Wm1Mp7qHLsFgixCGCayXJcT4mswo6V49faxHpZApQ'}, {'domain': '.apollo.io', 'expiry': 1728825223, 'httpOnly': False, 'name': 'intercom-device-id-dyws6i9m', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '6ff3ee0e-3b1c-4cf2-9c92-5bdb2b44a679'}, {'domain': 'app.apollo.io', 'httpOnly': True, 'name': '_leadgenie_session', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'px7j%2BQM8klhhR2h8B7QUZq1DAlVOtzyXukAFzVt89s%2FW4nEgPZqs7QzWyHc2qSj6QhrV44QTE6Nzj4NV9ycspS3cVlGt9W%2FnFFqWoyfrpGOy9N75s3LECYROurvqTmz%2FhMLRgW7O5KiHX15saCv4%2FOdNS7cRfdif7T0gAvgj7Hr4%2FD6ilZTygiAY90i1VQJFzI8Jn1UGPXE3BTPdjb0HMhipkBfhMeWhqFrBFb1ACJ8P0C%2BWXyFt5wqXpxbEpAky05GxjTnp7roMUA4roAgn3X0tebEds1Bbt6o%3D--hPUeFozDVLkDSJWC--mCnxl2Wc4EhUCDqrNUSwgg%3D%3D'}, {'domain': '.apollo.io', 'expiry': 1737031218, 'httpOnly': False, 'name': '_cioanonid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '29bb1576-a7a3-7747-02d2-72599f0eeed2'}, {'domain': '.app.apollo.io', 'expiry': 1737031223, 'httpOnly': False, 'name': '__stripe_mid', 'path': '/', 'sameSite': 'Strict', 'secure': True, 'value': '72346589-c2d0-4c50-aa8e-fe2ae896bfacc6d38c'}, {'domain': '.apollo.io', 'expiry': 1705497018, 'httpOnly': False, 'name': '__hssc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '21978340.1.1705495218857'}, {'domain': '.apollo.io', 'httpOnly': False, 'name': '__hssrc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': '.apollo.io', 'httpOnly': False, 'name': 'ZP_Pricing_Split_Test_Variant', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '23Q4_EC_Z59'}, {'domain': '.app.apollo.io', 'expiry': 1705497023, 'httpOnly': False, 'name': '__stripe_sid', 'path': '/', 'sameSite': 'Strict', 'secure': True, 'value': '9e001232-9357-444c-91b2-7e0a9f4ca2aeb5593c'}, {'domain': '.apollo.io', 'expiry': 1721047218, 'httpOnly': False, 'name': '__hstc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '21978340.c85064c479299d1e40a400ac39c9588b.1705495218857.1705495218857.1705495218857.1'}]
# ||||||||||||||||||||||||||||||------------End of Initialization------------||||||||||||||||||||||||||||||

# ||||||||||||||||||||||||||||||------------Start of Authentication Bypass------------||||||||||||||||||||||||||||||
driver.get(base_url)


for cookie in cookies:
    print("adding")
    driver.add_cookie(cookie)

try:
    printLogs(
        f"----------------------------------Start----------------------------------"
    )
    print(f"Hitting {base_url}...")
    printLogs(f"Hitting {base_url}...")
    driver.get(base_url)
    # ||||||||||||||||||||||||||||||------------End of Authentication Bypass------------||||||||||||||||||||||||||||||

    # ||||||||||||||||||||||||||||||------------Start of Domain lookup------------||||||||||||||||||||||||||||||
    search_box = driver.find_element(
        "xpath",
        "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/input",
    )
    search_box = driver.find_element(
        "xpath",
        "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/input",
    )
    search_box.send_keys(
        domain
    )  # Ahmed - Enter the organisation name into the search box
    time.sleep(3)

    # ||||||||||||||||||||||||||||||------------Start of Check if Search is giving up companies only------------||||||||||||||||||||||||||||||
    search_results = driver.find_elements(
        "xpath", "/html/body/div[7]/div/div/div/div/div/div/div/div"
    )
    if len(search_results) > 1:
        print("Decision b/w people and companies")
        printLogs("Decision b/w people and companies")
        search_result_section_id = 2
    # ||||||||||||||||||||||||||||||------------End of Check if Search is giving up companies only------------||||||||||||||||||||||||||||||

    list_of_companies = driver.find_elements(
        "xpath",
        f"/html/body/div[7]/div/div/div/div/div/div/div/div[{search_result_section_id}]/div",
    )
    for company in list_of_companies:
        print(
            driver.find_element(
                "xpath",
                f"/html/body/div[7]/div/div/div/div/div/div/div/div[{search_result_section_id}]/div[{company_index}]/div[3]",
            ).text
        )
        if (
            driver.find_element(
                "xpath",
                f"/html/body/div[7]/div/div/div/div/div/div/div/div/div[2]/div[3]/div/div",
            ).text
            == "Cold"
        ):
            cold_comapany = True
            driver.find_element(
                "xpath",
                f"html/body/div[7]/div/div/div/div/div/div/div/div/div[2]/div[3]/div/div",
            ).click()
            break
        if (
            driver.find_element(
                "xpath",
                f"html/body/div[7]/div/div/div/div/div/div/div/div/div[2]/div[3]/div/div",
            ).text
            == "New"
        ):
            cold_comapany = False
            driver.find_element(
                "xpath",
                f"/html/body/div[7]/div/div/div/div/div/div/div/div[{search_result_section_id}]/div[{company_index}]",
            ).click()
            break

        company_index = company_index + 1
    # /html/body/div[7]/div/div/div/div/div/div/div/div[{search_result_section_id}]/div[{company_index}]/div[3]
    print(f"Searching for {domain}...")
    printLogs(f"Searching for {domain}...")

    time.sleep(3)
    # ||||||||||||||||||||||||||||||------------End of Domain lookup------------||||||||||||||||||||||||||||||

    # ||||||||||||||||||||||||||||||------------Start of Decision Maker lookup------------||||||||||||||||||||||||||||||
    # /html/body/div[7]/div/div/div/div/div/div/div/div/div[2]/div[3]/div/div
    try:
        if driver.find_element(
            "xpath",
            "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a[4]",
        ):
            cold_comapany = True
        else:
            cold_comapany = False
    except:
        cold_comapany = False

    if cold_comapany:
        employees_btn = driver.find_element(
            "xpath",
            "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a[4]",
        )
    else:
        try:
            employees_btn = driver.find_element(
                "xpath",
                "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/a[4]",
            )
        except:
            # employees_btn = driver.find_element('xpath', '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/div/a[2]')
            employees_btn = driver.find_element(
                "xpath",
                "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/div/a[2]",
            )
    try:
            print("Trying to find the industry for this company")
            industry = driver.find_element("xpath","/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[2]/div/span").text
            print("HERE IS THE INDUSTRY")
            print(industry)
    except:
            print("failed to find industry")
    
    employees_btn.click()
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    
    time.sleep(3)
    length = 0
    if cold_comapany:
        try:
            #time.sleep(4)
            length_str = driver.find_element(
                "xpath",
                "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[3]/div/div[1]/span",
            ).text
            length = length_str.split(" of ")[1]
        except NoSuchElementException as ex:
            print("No Employee Found For this Cold Company")
            printLogs("No Employee Found For this Cold Company")
            result = subprocess.run(
                f"curl {hostname}/empty", shell=True, capture_output=True, text=True
            )
            print(f"Command output: {result.stdout}")
            printLogs(f"Command output: {result.stdout}")
            exit()

    else:
        try:
            #time.sleep(4)
            try:
                length_str = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div[1]/span",
                ).text
                length = length_str.split(" of ")[1]
            except:
                length_str = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[3]/div/div[1]/span",
                ).text
                length = length_str.split(" of ")[1]

        except NoSuchElementException as ex:
            print("No Employee Found for this New Company")
            printLogs("No Employee Found for this New Company")
            update_status(queue_id, "failed",cursor)
            result = subprocess.run(
                f"curl {hostname}/empty", shell=True, capture_output=True, text=True
            )

            print(f"Command output: {result.stdout}")
            printLogs(f"Command output: {result.stdout}")
            exit()

    no_of_pages = math.ceil(int(length.replace(",", "")) / 25)
    if no_of_pages > 5:
        no_of_pages = 5  # for free apollo

    for page_no in range(0, no_of_pages):
        print(f"Working on page number: {page_no}")
        printLogs(f"Working on page number: {page_no}")

        if page_no != 0:
            if cold_comapany:
                driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[3]/div/div[2]/button[2]",
                ).click()
            else:
                try:
                    driver.find_element(
                        "xpath",
                        "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[3]/div/div[2]/button[2]",
                    ).click()
                except:
                    driver.find_element(
                        "xpath",
                        "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div[2]/button[2]",
                    ).click()
            driver.switch_to.active_element.send_keys(Keys.ESCAPE)

            print("Changing page...")
            printLogs("Changing page...")
        

        time.sleep(3)
        if cold_comapany:
            all_employees = driver.find_element(
                "xpath",
                "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table",
            )
        else:
            try:
                all_employees = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table",
                )
            except:
                all_employees = driver.find_element(
                    "xpath",
                    "/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/table",
                )
        
        children_elements = all_employees.find_elements("xpath", "*")
        for i in range(0, len(children_elements)):
            driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            tbody = (children_elements[i].text).split("\n")
            quick_action_order = [
                check_column
                for check_column in column_checks
                if any(check_column.lower() in string.lower() for string in tbody)
            ]

            if quick_action_order:
                column_of_qck_act = tbody.index("Quick Actions") + 1

            found_words = [
                check_word
                for check_word in checks
                if any(check_word.lower() in string.lower() for string in tbody)
            ]
            print("here are the found words")
            print(found_words)
            for check_word in checks:
                if check_word.lower() in tbody[0].lower():
                    found_words.append(check_word)

            if found_words:
                print(f"Findings: {tbody}")
                printLogs(f"Findings: {tbody}")

                if cold_comapany:
                    if (
                        driver.find_element(
                            "xpath",
                            f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                        ).text
                    ).lower() == "access email":
                        driver.find_element(
                            "xpath",
                            f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                        ).click()

                    if (
                        driver.find_element(
                            "xpath",
                            f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                        ).text
                        != "Save Contact"
                    ):
                        save_contact = driver.find_element(
                            "xpath",
                            f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]/span/div/div/button[1]",
                        )
                        driver.switch_to.active_element.send_keys(Keys.ESCAPE)

                        print("COLD COMPANY")
                        driver.execute_script(
                            "arguments[0].scrollIntoView();", save_contact
                        )
                        save_contact.click()

                        try:
                            email = driver.find_element(
                                "xpath",
                                "/html/body/div[7]/div/div/div/div/div/div/div[2]/span",
                            ).text
                            print("EMAIL BELOW THIS LINES")
                            print(email)
                            print("EMAIL ABOVE THIS LINES")
                            # /html/body/div[7]/div/div/div/div/div/div/div[2]/span
                            found = {
                                "name": tbody[0],
                                "designation": (
                                    tbody[1]
                                    if ("---" not in tbody[1])
                                    else tbody[1] + tbody[2]
                                ),
                                "email": email,
                            }
                            if found not in findings:
                                findings.append(found)
                            found = {}
                        except NoSuchElementException as e:
                            print("Email element does not exist")
                            printLogs("Email element does not exist")
                else:
                    try:
                        print("NOT A COLD COMPANY")
                        if (
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).text
                        ).lower() == "access email":
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).click()

                        if (
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).text
                            != "Save Contact"
                        ):

                            save_contact = driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[4]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]/span/div/div/button[1]",
                            )
                            driver.switch_to.active_element.send_keys(Keys.ESCAPE)

                            driver.execute_script(
                                "arguments[0].scrollIntoView();", save_contact
                            )
                            save_contact.click()

                            try:
                                # /html/body/div[7]/div/div/div/div/div/div/div[1]/span --- previously yeh tha
                                # /html/body/div[7]/div/div/div/div/div/div/div[2]/span
                                email = driver.find_element(
                                    "xpath",
                                    "/html/body/div[7]/div/div/div/div/div/div/div[2]/span",
                                ).text
                                found = {
                                    "name": tbody[0],
                                    "designation": (
                                        tbody[1]
                                        if ("---" not in tbody[1])
                                        else tbody[1] + tbody[2]
                                    ),
                                    "email": email,
                                }
                                print(found not in findings)
                                if found not in findings:
                                    findings.append(found)
                                found = {}
                            except NoSuchElementException as e:
                                print("Email element does not exist")
                                printLogs("Email element does not exist")
                    except:
                        if (
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).text
                        ).lower() == "access email":
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).click()

                        if (
                            driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]",
                            ).text
                            != "Save Contact"
                        ):
                            time.sleep(3)
                            save_contact = driver.find_element(
                                "xpath",
                                f"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/table/tbody[{i}]/tr/td[{column_of_qck_act}]/span/div/div/button[1]",
                            )
                            driver.switch_to.active_element.send_keys(Keys.ESCAPE)

                            time.sleep(3)

                            driver.execute_script(
                                "arguments[0].scrollIntoView();", save_contact
                            )
                            save_contact.click()

                            try:
                                print("NOT A COLD COMPANY 2")
                                email = driver.find_element(
                                    "xpath",
                                    "/html/body/div[7]/div/div/div/div/div/div/div[2]/span",
                                ).text
                                found = {
                                    "name": tbody[0],
                                    "designation": (
                                        tbody[1]
                                        if ("---" not in tbody[1])
                                        else tbody[1] + tbody[2]
                                    ),
                                    "email": email,
                                }
                                print(found not in findings)
                                if found not in findings:
                                    findings.append(found)
                                found = {}
                            except NoSuchElementException as e:
                                print("Email element does not exist")
                                printLogs("Email element does not exist")

    # ||||||||||||||||||||||||||||||------------End of Decision Maker lookup------------||||||||||||||||||||||||||||||

    # ||||||||||||||||||||||||||||||------------JSON storage start------------||||||||||||||||||||||||||||||
    now = datetime.date.today()
    dt_string = now.strftime("%d-%m-%Y||%H:%M:%S")
    sitename = domain
    #update_status(queue_id, "test 1",cursor)
    if "https://" in sitename:
        sitename = sitename.replace("https://", "")
    elif "http://" in sitename:
        sitename = sitename.replace("http://", "")
    file_name = f"static/findings/{dt_string}-{sitename}.csv"
    provided_file = "findings.csv"
    df = pd.json_normalize(findings)
    print(findings)
    df.to_csv(provided_file, mode="w", index=False)
    result = subprocess.run(
        f"curl {hostname}/resource", shell=True, capture_output=True, text=True
    )
    print(f"findings right before updating status and adding to DB {findings}")
    #update_status(queue_id, "test 2",cursor)
    try:
        addResultsToDB(queue_id, findings, keyword, sitename,cursor,industry)
        update_status(queue_id, "completed",cursor)

    except Exception as e:
        update_status(queue_id,"DB ERROR",cursor)
    

    print(f"Command output: {result.stdout}")
    printLogs(f"Command output: {result.stdout}")
    print("Done!!")
    printLogs("Done!!")
    conn.commit()
    
    cursor.close()
    print(
        f"""This is the length of findings array in try
          {len(findings)}"""
    )
    printLogs(
        f"----------------------------------End----------------------------------"
    )
    # ||||||||||||||||||||||||||||||------------JSON storage end------------||||||||||||||||||||||||||||||

    driver.quit()
except Exception as e:
    print(
        "Error on line {}: {}, {}".format(
            sys.exc_info()[-1].tb_lineno, type(e).__name__, e
        )
    )
    print(
        f"""This is the length of findings array in catch
          {len(findings)}"""
    )
    # |||||||||||||||||| LOGIC FOR PARTIALLY RECIEVED RESULTS STARTS |||||||||||||||||||||
    if len(findings) >= 1:
        addResultsToDB(queue_id, findings, keyword, sitename,cursor,industry)
        update_status(queue_id, "partial",cursor)
    else:
        update_status(queue_id, "failed",cursor)
    # |||||||||||||||||| LOGIC FOR PARTIALLY RECIEVED RESULTS ENDS   |||||||||||||||||||||
    
    printLogs(
        f"Error on line {format(sys.exc_info()[-1].tb_lineno)} {type(e).__name__}"
    )
    result = subprocess.run(
        f"curl {hostname}/errored", shell=True, capture_output=True, text=True
    )
    conn.commit()

    cursor.close()
    print(f"Command output: {result.stdout}")
    printLogs(f"Command output: {result.stdout}")