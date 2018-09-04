from datetime import datetime
from configuration.config import Configuration  # imports Configuration file
import re               # For regular expression


class Validation:

    def string_validator(self, label, regex, max_length, alpha_special):
        while True:
            content = input('Enter ' + label + ':').strip()
            if alpha_special:
                result = re.findall(regex, content)
                if len(result) > 0:
                    print("Please enter " + label + " without ';' as this would affect the data")
                    continue
            else:
                result = bool(re.match(regex, content))
                if not result:
                    print("Please enter only alphanumeric characters")
                    continue
            if len(content) > max_length:
                print("Please enter " + label + " less than or equal to " + str(max_length) + " characters")
                continue
            else:
                return content

    def date_validator(self, label, start_date=datetime.now()):
        while True:
            date = input('Enter ' + label + '(DD/MM/YYYY):').strip()
            try:
                parsed_date = datetime.strptime(date, Configuration.date_format)
            except ValueError:
                print("Please enter date in DD/MM/YYYY format")
                continue
            if label == 'End Date':
                if parsed_date < start_date:
                    print("End date cannot be less than the start date")
                    continue
            if parsed_date > datetime.now():
                print("Future date is not allowed")
                continue
            else:
                return parsed_date

    def switch(self, argument, switcher):
        return switcher.get(argument, "nothing")

    def status_validator(self, label):
        while True:
            if label == 'Progress':
                status = int(input("Enter progress(1-2)\n1:Completed\n2:In-Progress\n").strip())
                result = Validation.switch(self, status, Configuration.switcher_progress)
            else:
                status = int(input("Enter confidence level(1-3)\n1:High\n2:Medium\n3:Low\n").strip())
                result = Validation.switch(self, status, Configuration.switcher_confidence)
            if result == "nothing":
                print("Please select number from the options given")
                continue
            else:
                return result









