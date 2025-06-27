from django.db import models

class MQTTMessage(models.Model):
    """
    用于存储MQTT消息的模型
    """
    topic = models.CharField(max_length=255, verbose_name='主题')
    payload = models.TextField(verbose_name='消息内容')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='接收时间')
    qos = models.IntegerField(default=0, verbose_name='服务质量',
                            help_text='MQTT服务质量等级(0, 1, 2)')

    class Meta:
        verbose_name = 'MQTT消息'
        verbose_name_plural = 'MQTT消息'
        ordering = ['-timestamp']  # 按时间倒序排列

    def __str__(self):
        return f"{self.topic} - {self.timestamp}"