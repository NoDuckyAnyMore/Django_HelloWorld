from django.urls import path, include
from . import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import MQTTMessageViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="这是你的接口文档",
        terms_of_service="https://www.example.com",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

 

# 创建路由器并注册MQTT消息视图集
router = DefaultRouter()
router.register(r'mqtt-messages', MQTTMessageViewSet)

urlpatterns = [
    path('helloWorld/', views.get_helloWorld, name='hello_world'),
    path('goods/', views.goods_list, name='get_data'),
    path('goods/<int:id>/', views.goods_detail, name='goods_detail'),
    path('', include(router.urls)),  # 包含路由器的URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # 可选添加 Redoc 风格文档：
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]  