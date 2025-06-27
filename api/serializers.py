from rest_framework import serializers
from goods.models import Goods
from mqtt_client.models import MQTTMessage

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__' 

class MQTTMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MQTTMessage
        fields = ['id', 'topic', 'payload', 'qos', 'timestamp']
        read_only_fields = ['id', 'timestamp']
        