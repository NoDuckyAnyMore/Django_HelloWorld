from django.apps import AppConfig


class MqttClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_client'

    def ready(self):
        """
        当Django应用准备就绪时，启动MQTT客户端
        """
        # 导入信号处理器
        import mqtt_client.signals
        
        # 直接启动MQTT客户端
        import os
        import sys
        
        # 只在runserver命令中启动MQTT客户端
        # 避免在其他Django命令行工具中启动
        # 使用RUN_MAIN环境变量避免在Django开发服务器的自动重载过程中重复连接
        if 'runserver' not in sys.argv:
            return
            
        # 避免在Django开发服务器的自动重载过程中重复连接
        if os.environ.get('RUN_MAIN') != 'true':
            return
            
        try:
            from .mqtt import mqtt_client
            mqtt_client.connect()
            print("MQTT client connected on application startup")
        except Exception as e:
            print(f"Failed to connect MQTT client: {e}")