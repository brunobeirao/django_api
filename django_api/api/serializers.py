from rest_framework import serializers
from .models import Call, CallBills, Charges


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallBills
        fields = ('id', 'price', 'duration')


class CallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = 'id', 'record_start', 'record_stop', 'source', 'destination'

    def create(self, validated_data):
        call = Call.objects.create(**validated_data)

        return validated_data


class CallsApiSerializer(serializers.Serializer):
    data = serializers.JSONField(required=False)

    def create(self, validated_data):
        call = Call.objects.create(**validated_data)
        return validated_data


class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = 'id', 'standing_charge', 'call_charge', 'useful_day'
