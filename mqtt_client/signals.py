from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def start_mqtt_client(sender, **kwargs):
    """
    在数据库迁移完成后启动MQTT客户端
    这是一个备用方法，主要的MQTT客户端启动逻辑在apps.py中
    """
    # 避免循环导入
    from .mqtt import mqtt_client
    
    # 只在mqtt_client应用迁移后启动
    if sender.name == 'mqtt_client':
        try:
            # 检查MQTT客户端是否已经连接
            if not mqtt_client.client.is_connected():
                mqtt_client.connect()
                print("MQTT client started after migration")
        except Exception as e:
            print(f"Failed to start MQTT client: {e}")