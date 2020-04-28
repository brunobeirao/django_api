import dateutil.parser

from datetime import datetime, timedelta

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .models import Call, CallBills, Charges


class ApiService:

    def __init__(self, params):
        self.call_id = params.get('call_id')
        self.start = params.get('start')
        self.stop = params.get('stop')

    def process_calls(self):
        try:
            start_record = dateutil.parser.parse(self.start['record_timestamp'])
            record_start = self.start['record_timestamp']
            record_stop = self.stop['record_timestamp']

            call = {
                'id': self.call_id,
                'source': self.start['source'],
                'destination': self.start['destination'],
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
        except IntegrityError as e:
            raise IntegrityError(e.args[0])
        except KeyError as key:
            raise KeyError(key.args[0])
        except Exception as ex:
            raise Exception(ex.args[0])

    @staticmethod
    def calculate_duration(days_diff):
        hours, remainder = divmod(days_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))

    def calculate_bills(self, start_record, stop_record):
        try:
            charge = ChargeService.get_charge_activated()
            start_record = dateutil.parser.parse(start_record)
            stop_record = dateutil.parser.parse(stop_record)
            days_diff = stop_record - start_record

            if days_diff.days != 0:
                start_record += timedelta(days=days_diff.days)
                start_date, stop_date = self.set_time(start_record, stop_record)

                minutes_day = (days_diff.days * charge.useful_day) * 60
                minutes_remaining = (stop_date - start_date).total_seconds() / 60
                minutes = minutes_day + minutes_remaining
                price = (minutes * charge.call_charge) + charge.standing_charge
            else:
                start_date, stop_date = self.set_time(start_record, stop_record)
                minutes = (stop_date - start_date).total_seconds() / 60
                price = (minutes * charge.call_charge) + charge.standing_charge

            return round(price, 2), days_diff

        except Exception as e:
            raise Exception('Calculate bills erro - ' + e.args[0])

    def set_time(self, start_record, stop_record):
        start_date = self.set_start_time(start_record)
        stop_date = self.set_stop_time(stop_record)
        return start_date, stop_date

    @staticmethod
    def set_start_time(start_record):
        if start_record.hour < 6:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=6, minute=00, second=00)
        elif start_record.hour > 22:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=22, minute=00, second=00)
        else:
            start_date = datetime.strptime(str(start_record), '%Y-%m-%d %H:%M:%S+00:00')
        return start_date

    @staticmethod
    def set_stop_time(stop_record):
        if stop_record.hour < 6:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=6, minute=00, second=00)
        elif stop_record.hour > 22:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=22, minute=00, second=00)
        else:
            stop_date = datetime.strptime(str(stop_record), '%Y-%m-%d %H:%M:%S+00:00')
        return stop_date

    @staticmethod
    def get_call(id):
        call = Call.objects.filter(id=id).select_related('callbills')
        return call


class ChargeService:

    def __init__(self, params):
        self.standing_charge = params.get('standing_charge')
        self.call_charge = params.get('call_charge')
        self.useful_day = params.get('useful_day')
        self.status = params.get('status')

    def save_charge(self):
        charge_activated = Charges.objects.filter(status=True).first()
        try:
            if charge_activated:
                self._update_status(charge_activated.id, False)
            self._save()
        except IntegrityError as e:
            self._update_status(charge_activated.id, True)
            raise IntegrityError(e.args[0])
        except ValueError:
            self._update_status(charge_activated.id, True)
            raise ValueError('Value must be with dot and not comma - Like: 0.55')

    def update_charge(self):
        charge = self.get_charge(self.standing_charge, self.call_charge)
        try:
            if self.status:
                self._update_status(charge.id, False)
            if charge:
                self._update(charge)
        except IntegrityError as e:
            self._update_status(charge.id, True)
            raise IntegrityError(e.args[0])
        except ValueError:
            self._update_status(charge.id, True)
            raise ValueError('Value must be with dot and not comma - Like: 0.55')

    def _save(self):
        charges = {
            'standing_charge': float(self.standing_charge),
            'call_charge': float(self.call_charge),
            'useful_day': int(self.useful_day),
            'status': True,
            'create_date': datetime.now()
        }
        charges = Charges(**charges)
        charges.save()

    def _update(self, charge_exists):
        Charges.objects.filter(id=charge_exists.id).update(
            standing_charge=self.standing_charge,
            call_charge=self.call_charge,
            useful_day=self.useful_day,
            status=bool(self.status))

    @staticmethod
    def get_charge(standing_charge, call_charge):
        return get_object_or_404(Charges, standing_charge=standing_charge, call_charge=call_charge)

    @staticmethod
    def get_charge_activated():
        return Charges.objects.get(status=True)

    @staticmethod
    def get_charge(standing_charge, call_charge):
        return get_object_or_404(Charges, standing_charge=standing_charge, call_charge=call_charge)

    @staticmethod
    def _update_status(id_charge, is_active):
        return Charges.objects.filter(id=id_charge).update(status=is_active)
