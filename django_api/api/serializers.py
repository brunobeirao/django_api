from rest_framework import serializers

from .models import Call, CallBills, Charges


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallBills
        fields = ('id', 'price', 'duration')


class CallsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    call_bills = BillsSerializer(many=False, read_only=True)

    class Meta:
        model = Call
        fields = ('id', 'record_start', 'record_stop', 'source', 'destination', 'call_bills')


class CallsApiSerializer(serializers.Serializer):
    json_data = serializers.JSONField(required=True)

    def create(self, validated_data):
        Call.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        pass


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = 'id', 'standing_charge', 'call_charge', 'useful_day', 'status'
