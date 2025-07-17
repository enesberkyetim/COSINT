# Generates the strings to be used for query in search engines
class Dorker :
    def __init__(self):
        pass
    # Generates LinkedIn related search strings
    def wrap_linkedin(self, company_name, domain_name):
        company_search = "site:linkedin.com/company \"" + company_name + "\""
        employee_search = "site:linkedin.com/in \"" + company_name + "\""
        mail_search = "site:linkedin.com/ \"" + "@" + domain_name + "\""

        return {"Company" : company_search, "Employee" : employee_search, "Mail" : mail_search}


    # To be completed, not yet
    def mail_guesser(self, employee_name, domain_name):
        results = []
        base = "@" + domain_name