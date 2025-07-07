import requests
from bs4 import BeautifulSoup
import lxml
import argparse

class CLI :
    def __init__(self, args):
        self.dorker = Dorker()
        self.args = args

        self.greet()
        print(self.dorker.wrap_linkedin(args.company, args.domain))
        pass

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

class Dorker :
    def __init__(self):
        pass
    def wrap_linkedin(self, company_name, domain_name):
        company_search = "site:linkedin.com/company \"" + company_name + "\""
        employee_search = "site:linkedin.com/in \"" + company_name + "\""
        mail_search = "site:linkedin.com/ \"" + "@" + domain_name + "\""

        return [company_search, employee_search, mail_search]


    # To be completed, not yet
    def mail_guesser(self, employee_name, domain_name):
        results = []
        base = "@" + domain_name



if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company", type=str, help="Company Name", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output File Name", required=False)
    parser.add_argument("-d", "--domain", type=str, help="Domain Name", required=True)
    args = parser.parse_args()

    cli = CLI(args)