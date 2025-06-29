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
        
        # 检查是否在特定的Django管理命令中运行（如migrate, collectstatic等）
        # 只排除这些特定命令，允许runserver和gunicorn等环境
        management_commands = ['migrate', 'makemigrations', 'collectstatic', 'test', 'shell']
        if len(sys.argv) > 1 and any(cmd in sys.argv for cmd in management_commands):
            return
            
        # 在开发服务器中避免重复连接（只在主进程中启动一次）
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return
        
        # 在Gunicorn环境中中避免重复连接（只在主进程中启动一次）

            
        # 添加日志记录
        import logging
        logger = logging.getLogger(__name__)
        
        # 检查是否在Gunicorn环境中运行
        if 'gunicorn' in sys.modules:
            # 在Gunicorn环境中，使用文件锁确保只有一个进程启动MQTT客户端
            import tempfile
            import fcntl
            
            pid = os.getpid()
            lock_file_path = os.path.join(tempfile.gettempdir(), 'django_mqtt_lock')
            
            try:
                # 尝试获取文件锁
                lock_file = open(lock_file_path, 'w')
                try:
                    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    # 成功获取锁，写入PID并启动MQTT客户端
                    lock_file.write(str(pid))
                    lock_file.flush()
                    logger.info(f"Process {pid} acquired lock and will start MQTT client")
                    
                    # 启动MQTT客户端
                    logger.info("Attempting to start MQTT client in Gunicorn environment")
                    try:
                        from .mqtt import mqtt_client
                        mqtt_client.connect()
                        logger.info("MQTT client successfully connected on application startup")
                    except Exception as e:
                        logger.error(f"Failed to connect MQTT client: {e}", exc_info=True)
                except IOError:
                    # 无法获取锁，说明已有其他进程启动了MQTT客户端
                    logger.info(f"Process {pid} will not start MQTT client, already started by another process")
                    lock_file.close()
            except Exception as e:
                logger.error(f"Error with lock file: {e}", exc_info=True)
        else:
            # 非Gunicorn环境，直接启动MQTT客户端
            logger.info("Attempting to start MQTT client in Runserver")
            try:
                from .mqtt import mqtt_client
                mqtt_client.connect()
                logger.info("MQTT client successfully connected on application startup")
            except Exception as e:
                logger.error(f"Failed to connect MQTT client: {e}", exc_info=True)
                # 不抛出异常，让应用继续启动，但记录错误