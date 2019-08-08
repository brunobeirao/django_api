from rest_framework import serializers
from .models import Call, CallBills


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
