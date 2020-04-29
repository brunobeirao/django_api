from rest_framework import serializers

from .models import Call, Bill, Charge


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = 'id', 'price', 'duration'


class CallSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    callbill = BillSerializer(many=False, read_only=True)

    class Meta:
        model = Call
        fields = 'id', 'record_start', 'record_stop', 'source', 'destination', 'callbill'


class CallApiSerializer(serializers.Serializer):
    json_data = serializers.JSONField(required=True)

    def create(self, validated_data):
        Call.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        pass


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = 'id', 'standing_charge', 'call_charge', 'hour_start', 'hour_stop', 'active'
