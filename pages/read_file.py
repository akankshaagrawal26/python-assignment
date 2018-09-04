from configuration.config import Configuration
from datetime import datetime
from pages.daily_status_report import DailyStatusReport


class ReadStatus:

    def read_file(self):
        """
        Function to read Daily Status Report file and send email of In-Progress status
        """
        temp_list = []
        in_progress_list = []
        dsr = DailyStatusReport()

        # Reading the file and appending data to list
        try:
            with open(Configuration.file_name,'r') as read_file:
                for line in read_file:
                    temp_list.append(line.replace("\n", "").split(Configuration.delimiter))
                read_file.close()
        except IOError as io:
            print(io)
        except Exception as e:
            print(e)
        finally:
            read_file.close()

        # Checks "In Progress Status" data in temp_list and add to another list
        for data in temp_list:
            if "In-Progress" in data:
                if datetime.strptime(data[3], Configuration.date_format) < datetime.now():
                    in_progress_list.append(data)
        print("In-progress list:", in_progress_list)

        # Call to send_mail function for sending In-Progress Status Report
        dsr.send_mail(in_progress_list)


# Creating object 'read_status' to call read_file Function of ReadStatus class
read_status = ReadStatus()
read_status.read_file()