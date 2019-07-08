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

        ini = self.start['record_timestamp']
        yourdate = dateutil.parser.parse(ini)
        # a = datetime.strptime(yourdate, '%Y-%m-%d %H:%M:%S')
        b = yourdate.hour
        # if self.start.hour > 6 and self.stop.hour < 22:


        return 'ok'
