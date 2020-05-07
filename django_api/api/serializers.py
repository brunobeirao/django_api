from rest_framework import serializers

from .models import Call, Bill, Charge


class CallSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    record_start = serializers.DateTimeField(required=False)
    record_stop = serializers.DateTimeField(required=False)
    # source = serializers.IntegerField(required=False)
    destination = serializers.IntegerField(required=False)
    duration = serializers.CharField(required=False)

    class Meta:
        model = Call
        fields = '__all__'


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


class BillSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(required=False)
    bill_call = CallSerializer(many=True, read_only=True )
    bill_charge = ChargeSerializer(many=False, read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'
