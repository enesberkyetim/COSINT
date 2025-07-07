import os
import shutil
import sys
from zipfile import ZipFile
import requests
import argparse
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class CLI :
    def __init__(self, args):
        self.dorker = Dorker()
        self.query_maker = QueryMaker()
        self.greet()
        self.get_chromedriver()
        self.print_linkedin()


    def get_chromedriver(self):
        if getattr(sys, 'frozen', False):
            chromedriver_def_path = os.path.join(sys._MEIPASS)
        else:
            chromedriver_def_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        version_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        version = requests.get(version_url).text

        url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/win64/chromedriver-win64.zip"

        zip_name = "chromedriver-win64.zip"

        zip_file_path = os.path.join(chromedriver_def_path, zip_name)

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(zip_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            pass

        try:
            with ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(chromedriver_def_path)

        except Exception as e:
            pass

        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)


        exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64/chromedriver.exe")

        try:
            shutil.copy(exact_path, chromedriver_def_path)
        except:
            pass

        exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64")

        try:
            shutil.rmtree(exact_path)
        except:
            pass

    # Greets the users on CLI
    def greet(self):
        headline = """
  ______    ______    ______   ______  __    __  ________
 /      \\  /      \\  /      \\ |      \\|  \\  |  \\|        \\
|  $$$$$$\\|  $$$$$$\\|  $$$$$$\\ \\$$$$$$| $$\\ | $$ \\$$$$$$$$
| $$   \\$$| $$  | $$| $$___\\$$  | $$  | $$$\\| $$   | $$
| $$      | $$  | $$ \\$$    \\   | $$  | $$$$\\ $$   | $$
| $$   __ | $$  | $$ _\\$$$$$$\\  | $$  | $$\\$$ $$   | $$
| $$__/  \\| $$__/ $$|  \\__| $$ _| $$_ | $$ \\$$$$   | $$
 \\$$    $$ \\$$    $$ \\$$    $$|   $$ \\| $$  \\$$$   | $$
  \\$$$$$$   \\$$$$$$   \\$$$$$$  \\$$$$$$ \\$$   \\$$    \\$$  \n"""

        print("\033[36m" + headline + "\033[0m")

        title = "\033[31m" + "Company Open Source Intelligence" + "\033[0m"
        print(f"{title:^67}")
        signature = "\033[31m" + "by karmagedon" + "\033[0m"
        print(f"{signature:^67}")
        version = "\033[31m" + "v.0.0" + "\033[0m"
        print(f"{version:^67}")

    def print_linkedin(self):
        linkedin_wordlist = self.dorker.wrap_linkedin(args.company, args.domain)
        self.query_maker.linkedin_query(linkedin_wordlist)

# Generates the strings to be used for query in search engines
class Dorker :
    def __init__(self):
        pass
    # Generates LinkedIn related search strings
    def wrap_linkedin(self, company_name, domain_name):
        company_search = "site:linkedin.com/company \"" + company_name + "\""
        employee_search = "site:linkedin.com/in \"" + company_name + "\""
        mail_search = "site:linkedin.com/ \"" + "@" + domain_name + "\""

        return [company_search, employee_search, mail_search]


    # To be completed, not yet
    def mail_guesser(self, employee_name, domain_name):
        results = []
        base = "@" + domain_name

class QueryMaker :
    def __init__(self):
        pass
    def linkedin_query(self, wordlist):
        employees = self.linkedin_employee_query(wordlist)
        mails = self.linkedin_mail_query(wordlist)
        company_info = self.linkedin_company_query(wordlist)
        return {"Employees" : employees, "Mails" : mails, "Company" : company_info}

    def linkedin_employee_query(self, wordlist):

        for query in wordlist:
            user_agent = UserAgent()
            random_agent = user_agent.random

            request_headers = {"user-agent" : random_agent}

            url = f"https://www.bing.com/search?q={query}"

    def linkedin_company_query(self, wordlist):
        pass
    def linkedin_mail_query(self, wordlist):
        pass



if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company", type=str, help="Company Name", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output File Name", required=False)
    parser.add_argument("-d", "--domain", type=str, help="Domain Name", required=True)
    args = parser.parse_args()

    cli = CLI(args)