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
        duration = self.calculate_duration(days_diff)

        bill = {
            'price': price,
            'call_start_date': start_record.date(),
            'call_start_time': start_record.time(),
            'duration': duration,
            'call': call

        }
        bill = CallBills(**bill)
        bill.save()

        print("Salvo")

    @staticmethod
    def calculate_duration(days_diff):
        hours, remainder = divmod(days_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))

    def calculate_bills(self, start_record, stop_record):
        standing_charge = 0.36
        call_charge = 0.09
        useful_day = 16

        start_record = dateutil.parser.parse(start_record)
        stop_record = dateutil.parser.parse(stop_record)
        days_diff = stop_record - start_record

        if days_diff.days != 0:
            start_record += timedelta(days=days_diff.days)
            start_date, stop_date = self.set_time(start_record, stop_record)

            minutes_day = (days_diff.days * useful_day) * 60
            minutes_remaining = (stop_date - start_date).total_seconds() / 60
            minutes = minutes_day + minutes_remaining
            price = (minutes * call_charge) + standing_charge
        else:
            start_date, stop_date = self.set_time(start_record, stop_record)
            minutes = (stop_date - start_date).total_seconds() / 60
            price = (minutes * call_charge) + standing_charge

        return round(price, 2), days_diff

    def set_time(self, start_record, stop_record):
        start_date = self.set_start_time(start_record)
        stop_date = self.set_stop_time(stop_record)
        return start_date, stop_date

    @staticmethod
    def set_start_time(start_record):
        if start_record.hour < 6:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S%z')\
                .replace(hour=6, minute=00, second=00)
        elif start_record.hour > 22:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S%z')\
                .replace(hour=22, minute=00, second=00)
        else:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S%z')
        return start_date

    @staticmethod
    def set_stop_time(stop_record):
        if stop_record.hour < 6:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S%z')\
                .replace(hour=6, minute=00, second=00)
        elif stop_record.hour > 22:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S%z')\
                .replace(hour=22, minute=00, second=00)
        else:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S%z')
        return stop_date
