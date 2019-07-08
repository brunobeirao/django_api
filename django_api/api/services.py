from datetime import datetime
import dateutil.parser



class ApiService:
    def __init__(self, params):
        self.call_id = params.get('call_id')
        self.start = params.get('start')
        self.stop = params.get('stop')

    def calculate_bills(self):
        standing_charge = 0.36
        call_charge = 0.09

        start_hour = dateutil.parser.parse(self.start['record_timestamp'])
        stop_hour = dateutil.parser.parse(self.stop['record_timestamp'])
        # a = datetime.strptime(yourdate, '%Y-%m-%d %H:%M:%S')
        # b = yourdate.hour
        if start_hour.hour > 6 and stop_hour.hour <= 22:
            print("X")
            if stop_hour.hour == 22:

                stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(minute=00)

            seconds = (stop_hour - start_hour).total_seconds()
            minutes = seconds/60

            price = minutes * call_charge + standing_charge
        elif start_hour.hour > 22 and stop_hour.hour < 6:
            print("Y")
            seconds = (stop_hour - start_hour).total_seconds()
            minutes = seconds / 60
            price = 0.36
        else:
            print("Z")

        return 'ok'
