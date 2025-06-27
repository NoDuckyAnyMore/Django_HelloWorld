from django.contrib import admin
from .models import MQTTMessage

@admin.register(MQTTMessage)
class MQTTMessageAdmin(admin.ModelAdmin):
    """
    MQTT消息的管理界面配置
    """
    list_display = ('topic', 'payload', 'qos', 'timestamp')
    list_filter = ('topic', 'timestamp')
    search_fields = ('topic', 'payload')
    readonly_fields = ('timestamp',)