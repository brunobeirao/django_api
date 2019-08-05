from rest_framework import serializers
from .models import Call, CallBills

class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallBills
        fields = ('id', 'price', 'duration')


class CallsApiSerializer(serializers.ModelSerializer):
    print("destination")
    # start = StartSerializer(many=False)
    # stop = StopSerializer(many=False)

    class Meta:
        model = Call
        fields = 'id', 'record_start', 'record_stop', 'source', 'destination'

    def create(self, validated_data):
        # start = validated_data.pop('start')
        # stop = validated_data.pop('stop')
        call = Call.objects.create(**validated_data)
        # StartCallRecord.objects.create(call=call, **start)
        # StopCallRecord.objects.create(call=call, **stop)
        return validated_data


class CallUploadSerializer(serializers.Serializer):
    data = serializers.JSONField(required=False)

    def create(self, validated_data):
        return validated_data
