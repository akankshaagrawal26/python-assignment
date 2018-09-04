from pages.daily_status_report import DailyStatusReport


class Main:

    def main(self):
        """
        Main function to get the daily status from the user, read the status,
        write the status to file and mail the status of the report
        """

        dsr = DailyStatusReport()       # Creating object 'dsr' of DailyStatusReport class
        headers = dsr.get_headers()
        data = dsr.get_data()
        final_list = dsr.write_file(headers, data)
        dsr.send_mail(final_list)


# Creating object 'mainObj' to call main Function
mainObj = Main()
mainObj.main()





