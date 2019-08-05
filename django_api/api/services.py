from datetime import datetime, timedelta
import dateutil.parser
from .models import Call, CallBills


class ApiService:
    def __init__(self, params):
        self.call_id = params.get('call_id')
        self.start = params.get('start')
        self.stop = params.get('stop')

    def save_start_call(self):
        start_record = dateutil.parser.parse(self.start['record_timestamp'])
        call_id = self.call_id
        source = self.start['source']
        destination = self.start['destination']
        record_start = self.start['record_timestamp']
        record_stop = self.stop['record_timestamp']

        call = {
            'id': call_id,
            'source': source,
            'destination': destination,
            'record_start': record_start,
            'record_stop': record_stop

        }
        call = Call(**call)
        call.save()

        price, days_diff = self.calculate_bills(record_start, record_stop)

        bill = {
            'price': price,
            'call_start_date': start_record.date(),
            'call_start_time': start_record.time(),
            'duration': days_diff,
            'call': call

        }
        bill = CallBills(**bill)
        bill.save()

        print("a")

    def calculate_bills(self, start_record, stop_record):
        standing_charge = 0.36
        call_charge = 0.09
        useful_day = 16

        start_record = dateutil.parser.parse(start_record)
        stop_record = dateutil.parser.parse(stop_record)

        # if same day simple verification
        # else calculate days and hours
        # subtracao para pegar a diferenca
        days_diff = stop_record - start_record

        # se existir diferenca de dias start stop
        if days_diff.days != 0:
            start_record += timedelta(days=days_diff.days)
            start_date, stop_date = self.calcule_hour(start_record, stop_record)

            minutes_day = (days_diff.days * useful_day) * 60
            minutes_remaining = (stop_date - start_date).total_seconds() / 60
            minutes = minutes_day + minutes_remaining
            price = (minutes * call_charge) + standing_charge

            hours, remainder = divmod(days_diff.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)

            # dt = datetime.strptime('40:00:15', "%H:%M:%S")
            # td = timedelta(hours=hours, minutes=minutes, seconds=seconds).
            # days_diff = str(int(hours) + ':' + int(minutes) + ':' + int(seconds))
            # t = datetime.strptime("05:20:25", "%H:%M:%S").replace(hour=int(hours), minute=int(minutes), second=int(seconds))
            print(0)
        else:
            start_date, stop_date = self.calcule_hour(start_record, stop_record)
            minutes = (stop_date - start_date).total_seconds() / 60
            price = (minutes * call_charge) + standing_charge

        return round(price, 2), days_diff

    def calcule_hour(self, start_record, stop_record):
        if start_record.hour < 6:
            start_date = datetime.strptime(str(start_record), "%Y-%m-%d %H:%M:%S+00:00").replace(hour=6, minute=00,
                                                                                                 second=00)
        elif start_record.hour > 22:
            start_date = datetime.strptime(str(start_record), "%Y-%m-%dT%H:%M:%SZ").replace(hour=22, minute=00, second=00)
        else:
            start_date = datetime.strptime(str(start_record), "%Y-%m-%dT%H:%M:%SZ")

        if stop_record.hour < 6:
            stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=6, minute=00,
                                                                                                       second=00)
        elif stop_record.hour > 22:
            stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ").replace(hour=22, minute=00,
                                                                                                       second=00)
        else:
            stop_date = datetime.strptime(self.stop['record_timestamp'], "%Y-%m-%dT%H:%M:%SZ")

        return start_date, stop_date
