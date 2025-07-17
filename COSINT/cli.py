import os
import shutil
import sys
from zipfile import ZipFile
import requests
import argparse
import platform
from time import sleep

from dorker import Dorker
from querymaker import QueryMaker


# Responsible for CLI and also orchestrating the main functions
class CLI :
    def __init__(self, args):
        self.args = args
        self.linkedin_results
        self.greet()
        self.dorker = Dorker()
        self.chromedriver_def_path = self.get_chromedriver()
        self.query_maker = QueryMaker(self.chromedriver_def_path, self.args.pagenumber, self.args.headless)
        self.print_linkedin()

    # Downloads chromedriver's latest release from the internet according to the host OS
    def get_chromedriver(self):
        """
        If I use general path convention, it won't work when we extract this project
        to an executable file. So I decide the path to main.py like this
        """
        if getattr(sys, 'frozen', False):
            chromedriver_def_path = os.path.join(sys._MEIPASS)
        else:
            chromedriver_def_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        # Checking and getting the latest version number
        version_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        version = requests.get(version_url).text

        # Paths and executable names differ from OS to OS. So I branched them
        if (platform.system() == "Windows"):
            # chromedriver's download links are following a general pattern
            url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/win64/chromedriver-win64.zip"
            zip_name = "chromedriver-win64.zip"

            zip_file_path = os.path.join(chromedriver_def_path, zip_name)

            # Downloading the latest chromedriver zip file
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(zip_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                print("ChromeDriver download failed")
                raise SystemExit(1)

            # Extracting the zip file
            try:
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(chromedriver_def_path)

            except Exception as e:
                print(e)
                raise SystemExit(1)

            # Removing the zip file because it's extracted already
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64/chromedriver.exe")

            # We need only the chromedriver from the extracted folder so we copy it outside the folder
            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-win64")

            # Removing the extracted folder recursively
            try:
                shutil.rmtree(exact_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            return chromedriver_def_path + "/chromedriver.exe"

        # Similar things goes on Linux part
        elif (platform.system() == "Linux") :
            url = "https://storage.googleapis.com/chrome-for-testing-public/" + version + "/linux64/chromedriver-linux64.zip"
            zip_name = "chromedriver-linux64.zip"
            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64/chromedriver") # bak

            zip_file_path = os.path.join(chromedriver_def_path, zip_name)

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(zip_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                raise SystemExit(1)

            try:
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(chromedriver_def_path)

            except Exception as e:
                print(e)
                raise SystemExit(1)

            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64/chromedriver")

            try:
                shutil.copy(exact_path, chromedriver_def_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            exact_path = os.path.join(chromedriver_def_path, "chromedriver-linux64")

            try:
                shutil.rmtree(exact_path)
            except Exception as e:
                print(e)
                raise SystemExit(1)

            # Returning the path of the donwloaded chromedriver latest release
            return chromedriver_def_path + "/chromedriver"

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
        print()

    # Initiating the functions related to LinkedIn scraping
    def save_linkedin(self, list):
        self.linkedin_results = list
    def print_linkedin(self):
        linkedin_wordlist = self.dorker.wrap_linkedin(self.args.company, self.args.domain)
        employee_filtered_links = self.query_maker.linkedin_query(linkedin_wordlist).get("Employees")
        self.save_linkedin(employee_filtered_links)
        company_name = linkedin_wordlist.get("Company")

        temp1 = "Employee Name and Role"
        temp2 = "Link"
        print(f"{temp1:^80}", end='')
        print("|  ", end='')
        print(f"{temp2:^88}", end='')
        print("|")
        print("-" * 172)

        for linkedin_link in employee_filtered_links:
            full_string = linkedin_link[0]
            employee_name = full_string[0:full_string.index(" - ")]
            temp = full_string[full_string.index(" - ")+3:]
            try :
                employee_role = temp[0:temp.index(" - ")]
            except :
                try :
                    employee_role = temp[0:temp.index(" | ")]
                except:
                    employee_role = "Unknown"

            if (employee_role == company_name) :
                temp1 = "Unknown"
            else :
                temp1 = employee_role

            temp2 = linkedin_link[1]
            if (len(employee_name) >= 33) :
                employee_name = employee_name[:33]
            if (len(temp1) >= 43) :
                temp1 = employee_role[:43]
            print(f"{employee_name:<34}", end='')
            print("| ", end='')
            print(f"{temp1:<44}", end='')
            print("|", end='')
            print(f"{temp2:^90}", end='')
            print("|")
        print("Total results : ", len(employee_filtered_links))