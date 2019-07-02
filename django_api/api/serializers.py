from rest_framework import serializers
from .models import Calls


class CallsApiSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Calls
        fields = '__all__'
        read_only_fields = ('id', )
