import dateutil.parser

from datetime import datetime, timedelta

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .models import Call, Bill, Charge


class ApiService:

    def __init__(self, params):
        self.call_id = params.get('call_id')
        self.start = params.get('start')
        self.stop = params.get('stop')
        self.charge = ChargeService.get_charge_activated()

    def get_call(self, telephone_bill, year, month):
        value = self.get_telephone_bill(telephone_bill, year, month)
        return value

    def process_calls(self):
        try:
            record_start = self.start['record_timestamp']
            record_stop = self.stop['record_timestamp']

            price, days_diff = self.calculate_bills(record_start, record_stop)
            duration = self.calculate_duration(days_diff)

            call = {
                'id': self.call_id,
                'source': self.start['source'],
                'destination': self.start['destination'],
                'record_start': record_start,
                'record_stop': record_stop,
                'duration': duration,
            }
            call = Call(**call)
            call.save()

            bill = {
                'price': price,
                'call': call,
                'charge': self.charge,
            }
            bill = Bill(**bill)
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
            useful_day = self.charge.hour_stop - self.charge.hour_start;
            start_record = dateutil.parser.parse(start_record)
            stop_record = dateutil.parser.parse(stop_record)
            days_diff = stop_record - start_record

            if days_diff.days != 0:
                start_record += timedelta(days=days_diff.days)
                start_date, stop_date = self.set_time_record(start_record, stop_record)

                minutes_day = (days_diff.days * useful_day) * 60
                minutes_remaining = (stop_date - start_date).total_seconds() / 60
                minutes = minutes_day + minutes_remaining
                price = (int(minutes) * self.charge.call_charge) + self.charge.standing_charge
            else:
                start_date, stop_date = self.set_time_record(start_record, stop_record)
                minutes = (stop_date - start_date).total_seconds() / 60
                price = (int(minutes) * self.charge.call_charge) + self.charge.standing_charge

            return round(price, 2), days_diff
        except Exception as e:
            raise Exception('Calculate Bill error - ' + e.args[0])

    def set_time_record(self, start_record, stop_record):
        start_date = self.set_time(start_record)
        stop_date = self.set_time(stop_record)
        return start_date, stop_date

    def set_time(self, record):
        if record.hour < self.charge.hour_start:
            time = datetime.strptime(str(record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=self.charge.hour_start, minute=00, second=00)
        elif record.hour > self.charge.hour_stop:
            time = datetime.strptime(str(record), '%Y-%m-%d %H:%M:%S+00:00')\
                .replace(hour=self.charge.hour_stop, minute=00, second=00)
        else:
            time = datetime.strptime(str(record), '%Y-%m-%d %H:%M:%S+00:00')
        return time

    @staticmethod
    def get_telephone_bill(telephone_bill, year, month):
        if not month and not year:
            last_call = Call.objects.latest('record_stop')
            year = last_call.record_stop.year
            month = last_call.record_stop.month

        calls = Bill.objects.filter(call__source=telephone_bill,
                                    call__record_stop__year=year,
                                    call__record_stop__month=month) \
            .values('call__destination', 'call__record_start', 'call__duration', 'price')

        formatted_call_list = []
        for call in calls:
            formatted_call = {'destination': call['call__destination'], 'start_date': call['call__record_start'].date(),
                              'start_time': call['call__record_start'].time(), 'duration': call['call__duration'],
                              'price': call['price']}
            formatted_call_list.append(formatted_call)

        return formatted_call_list


class ChargeService:

    def __init__(self, params):
        self.standing_charge = params.get('standing_charge')
        self.call_charge = params.get('call_charge')
        self.hour_start = params.get('hour_start')
        self.hour_stop = params.get('hour_stop')
        self.active = params.get('active')

    def save_charge(self):
        charge_activated = Charge.objects.filter(active=True).first()
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
            if self.active:
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
        charge = {
            'standing_charge': float(self.standing_charge),
            'call_charge': float(self.call_charge),
            'hour_start': int(self.hour_start),
            'hour_stop': int(self.hour_stop),
            'active': True,
            'create_date': datetime.now()
        }
        charge = Charge(**charge)
        charge.save()

    def _update(self, charge_exists):
        Charge.objects.filter(id=charge_exists.id).update(
            standing_charge=self.standing_charge,
            call_charge=self.call_charge,
            hour_start=self.hour_start,
            hour_stop=self.hour_stop,
            active=bool(self.active))

    @staticmethod
    def get_charge(standing_charge, call_charge):
        return get_object_or_404(Charge, standing_charge=standing_charge, call_charge=call_charge)

    @staticmethod
    def get_charge_activated():
        return Charge.objects.get(active=True)

    @staticmethod
    def get_charge(standing_charge, call_charge):
        return get_object_or_404(Charge, standing_charge=standing_charge, call_charge=call_charge)

    @staticmethod
    def _update_status(id_charge, is_active):
        return Charge.objects.filter(id=id_charge).update(active=is_active)
