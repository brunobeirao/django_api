from datetime import datetime, timedelta
import dateutil.parser



class ApiService:
    def __init__(self, params):
        self.call_id = params.get('call_id')
        self.start = params.get('start')
        self.stop = params.get('stop')

    def calculate_bills(self):
        standing_charge = 0.36
        call_charge = 0.09

        start_record = dateutil.parser.parse(self.start['record_timestamp'])
        stop_record = dateutil.parser.parse(self.stop['record_timestamp'])


        # if same day simple verification
        # else calculate days and hours

        days = stop_record - start_record

        if days.days != 0:
            start_record += timedelta(days=days.days)
            if start_record.hour < 6:
                start_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=6)
            elif start_record.hour > 22:
                start_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=22)

            if stop_record.hour < 6:
                stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=6)
            elif stop_record.hour > 22:
                stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=22)

        # 1 dia = 16h taxada mais a diferença do start_date e stop_date

        seconds = (stop_record - start_record).total_seconds()
        #
        # minutes = seconds / 60

        # price = minutes * call_charge + standing_charge



        if start_record.day == stop_record.day:

            if start_record.hour > 6 and stop_record.hour <= 22:
                print("X")
                if stop_record.hour == 22:

                    stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(minute=00)

                seconds = (stop_record - start_record).total_seconds()
                minutes = seconds/60

                price = minutes * call_charge + standing_charge
            elif start_record.hour > 22 and stop_record.hour <= 6:
                print("Y")
                seconds = (stop_record - start_record).total_seconds()
                minutes = seconds / 60
                price = 0.36

            elif start_record.hour <= 6 and stop_record.hour > 6:
                start_date = datetime.strptime(self.start['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(minute=00)

                seconds = (stop_record - start_record).total_seconds()
                minutes = seconds / 60

                price = minutes * call_charge + standing_charge
            else:
                print("Z")
                #hora maior 6 e menor que 22
                if 22 > start_record.hour > 6:
                    test = start_record - 24
                    teste = test * -1

        return 'ok'
