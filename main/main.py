from pages.daily_status_report import DailyStatusReport
from pages.read_file import ReadStatus


class Main:

    def main(self):
        """
        Main function to get the daily status from the user, read the status,
        write the status to file and mail the status of the report
        """

        dsr = DailyStatusReport()       # Creating object 'dsr' of DailyStatusReport class
        headers = dsr.get_headers()
        data = dsr.get_data()
        dsr_input_data = dsr.write_file(headers, data)
        dsr.send_mail(dsr_input_data)


# Creating object 'mainObj' to call main Function
mainObj = Main()
mainObj.main()

# Send email for still In-Progress task
rs = ReadStatus()
rs.read_file()





