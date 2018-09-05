import os
import smtplib
from configuration.config import Configuration
from utility.validation import Validation
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class DailyStatusReport(Validation):

    def get_headers(self):
        """
        Function to get Header List
        """
        header_list = ["Topic", "Content", "Start Date", "End Date", "Progress", "Confidence Level", "Team Member",
                       "Comments"]
        return header_list

    def get_data(self):
        """
        Function to get Data List

        """
        data_list = []
        regex1 = r'[;]+'  # Regex for accepting AlphaNumeric+Special Characters except delimiter i.e ';'
        regex2 = r'[a-zA-Z0-9]+$'  # Regex for accepting AlphaNumeric only.

        try:
            topic = super(DailyStatusReport, self).string_validator('Topic', regex1, 255, True)
            data_list.append(topic)
            content = super(DailyStatusReport, self).string_validator('Content', regex1, 255, True)
            data_list.append(content)
            start_date = super(DailyStatusReport, self).date_validator('Start Date')
            format_start_date = start_date.strftime(Configuration.date_format)
            data_list.append(format_start_date)
            end_date = super(DailyStatusReport, self).date_validator('End Date', start_date)
            format_end_date = end_date.strftime(Configuration.date_format)
            data_list.append(format_end_date)
            progress = super(DailyStatusReport, self).status_validator('Progress')
            data_list.append(progress)
            confidence_level = super(DailyStatusReport, self).status_validator('Confidence Level')
            data_list.append(confidence_level)
            team_member = super(DailyStatusReport, self).string_validator('Team Member', regex2, 100, False)
            data_list.append(team_member)
            comments = super(DailyStatusReport, self).string_validator('Comments', regex1, 1024, True)
            data_list.append(comments)
            return data_list

        except Exception as e:
            print("Something went wrong while reading input", e)

    def write_file(self, headers, data):
        """
        Function to write status to the Daily Status Report file
        """

        final_list = []  # Appends Header and Data to the list
        try:
            with open(Configuration.file_name, 'a') as out:
                if os.path.getsize(Configuration.file_name) == 0:  # checks the size of the file is 0
                    final_list.append(headers)  # Appends headers to the final list
                final_list.append(data)  # Appends data to the final list
                for word in final_list:
                    out.write(Configuration.delimiter.join(word) + "\n")
                out.close()
                return final_list

        except IOError as io:
            print("IO Exception occurred", io)
        except Exception as e:
            print("Something went wrong while writing data to the file", e)
        finally:
            out.close()

    def send_mail(self, final_list, label='Daily Status'):
        """
        Function to send mail to the configured email id
        """
        try:
            smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.ehlo()
            smtp_obj.login(Configuration.server_login_email, Configuration.server_login_password)

            mail_from = Configuration.mail_from
            mail_to = Configuration.mail_to

            msg = MIMEMultipart()
            msg['From'] = mail_from
            msg['To'] = mail_to
            msg['Subject'] = "Daily Status Report"
            i = 0
            body = ""
            header = "<center><h1>Daily Status Report</h1><center><br><br><table style='width:100%'><tr>"
            fetch_header_list = self.get_headers()
            for head in fetch_header_list:
                header += "<th>" + head + "</th>"
            header += "</tr>"
            if label == 'Daily Status':
                if len(final_list) > 1:
                    i += 1
            while i < len(final_list):
                body += "<tr><td>" + final_list[i][0] + "</td><td>" + final_list[i][1] + "</td><td>" + \
                        final_list[i][2] + "</td><td>" \
                        + final_list[i][3] + "</td><td>" + final_list[i][4] + "</td><td>" + final_list[i][5] \
                        + "</td><td>" + final_list[i][6] + "</td><td>" + final_list[i][7] + "</td></tr>"
                i += 1
            content = header + body
            print("Complete content for mailing:", content)
            msg.attach(MIMEText(content, 'html'))
            text = msg.as_string()
            smtp_obj.sendmail(mail_from, mail_to, text)
            print("Status mail sent successfully")

        except smtplib.SMTPException as se:
            print("Unable to send mail", se)
        except Exception as e:
            print("Something went wrong while sending mail", e)

