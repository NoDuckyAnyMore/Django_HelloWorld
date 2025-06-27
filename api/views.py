from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.decorators import action

from api.serializers import GoodsSerializer, MQTTMessageSerializer
from goods.models import Goods
from mqtt_client.models import MQTTMessage


@api_view(['GET'])
def get_helloWorld(request):
    """
    A simple API view that returns a JSON response with a message.
    """
    data = {
        "message": "Hello, this is a response from the API!"
    }
    return Response(data)

@api_view(['GET', 'POST'])
def goods_list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'PUT', 'DELETE'])    
def goods_detail(request,id):
    try:
        goods = Goods.objects.get(id=id)
    except Goods.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GoodsSerializer(goods)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = GoodsSerializer(goods, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        goods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MQTTMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    MQTT消息的视图集
    提供只读访问，因为消息只能通过MQTT接收，不能通过API创建
    """
    queryset = MQTTMessage.objects.all().order_by('-timestamp')
    serializer_class = MQTTMessageSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        获取最新的MQTT消息
        """
        latest_message = self.get_queryset().first()
        if latest_message:
            serializer = self.get_serializer(latest_message)
            return Response(serializer.data)
        return Response({'message': 'No messages available'})

    @action(detail=False, methods=['get'])
    def by_topic(self, request):
        """
        按主题获取消息
        """
        topic = request.query_params.get('topic', None)
        if topic:
            messages = self.get_queryset().filter(topic=topic)
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        return Response({'error': 'Topic parameter is required'}, status=400)