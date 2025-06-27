import paho.mqtt.client as mqtt
from django.conf import settings
from django.utils import timezone
from .models import MQTTMessage
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # 如果配置了MQTT认证信息，设置用户名和密码
        if hasattr(settings, 'MQTT_USERNAME') and hasattr(settings, 'MQTT_PASSWORD'):
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def connect(self):
        """连接到MQTT broker"""
        try:
            # 从Django设置中获取MQTT broker的主机和端口
            host = getattr(settings, 'MQTT_BROKER_HOST', 'localhost')
            port = getattr(settings, 'MQTT_BROKER_PORT', 1883)
            
            print(f"Connecting to MQTT broker at {host}:{port}")
            self.client.connect(host, port, 60)
            self.client.loop_start()  # 在后台线程中启动网络循环
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            raise

    def on_connect(self, client, userdata, flags, rc):
        """当客户端连接到MQTT broker时的回调"""
        if rc == 0:
            print("Connected to MQTT broker")
            # 订阅配置的主题
            topics = getattr(settings, 'MQTT_TOPICS', ['#'])  # 默认订阅所有主题
            for topic in topics:
                self.client.subscribe(topic)
                print(f"Subscribed to topic: {topic}")
        else:
            print(f"Failed to connect to MQTT broker with code: {rc}")

    def on_message(self, client, userdata, msg):
        """当收到MQTT消息时的回调"""
        try:
            # 将消息保存到数据库
            payload = msg.payload.decode('utf-8')
            MQTTMessage.objects.create(
                topic=msg.topic,
                payload=payload,
                qos=msg.qos
            )
            print(f"Received message on topic {msg.topic} with QoS {msg.qos}: {payload}")
        except Exception as e:
            print(f"Error processing MQTT message: {e}")

    def on_disconnect(self, client, userdata, rc):
        """当客户端断开连接时的回调"""
        if rc != 0:
            print(f"Unexpected MQTT disconnection with code: {rc}. Will auto-reconnect.")

    def disconnect(self):
        """断开与MQTT broker的连接"""
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")

# 创建全局MQTT客户端实例
mqtt_client = MQTTClient()