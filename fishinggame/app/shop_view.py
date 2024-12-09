import json

import pika
import redis
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User, ShopItem, ShopedItem

# 连接 Redis 实例
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

# 消息队列连接设置
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='shop_purchase_queue')

class ShopPurchaseView(APIView):

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        user_id = request.data.get('user_id')
        item_name = request.data.get('item_name')
        category = request.data.get('category')

        # 设置 Redis 锁的 key，避免重复购买
        lock_key = f"shop_items_lock_{user_id}_{item_name}"
        lock = redis_instance.set(lock_key, 1, nx=True, ex=10)  # 锁定10秒，避免并发操作

        if not lock:
            return Response({"message": "Too many requests! Try again later!"}, status=429)

        try:
            # 查找用户
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return Response({"message": "User not found"}, status=404)

            # 查找商品（这里可以通过 Redis 缓存）
            cache_key = f"shop_item_{category}_{item_name}"
            item = cache.get(cache_key)
            if not item:
                item = ShopItem.objects.filter(category=category, name=item_name).first()
                if not item:
                    return Response({"message": "Item not found"}, status=404)
                # 缓存商品信息，缓存时间为10分钟
                cache.set(cache_key, item, timeout=600)

            # 确定货币类型并获取商品价格
            currency = determine_currency(category)
            price = getattr(item, currency)

            # 检查用户货币是否足够
            if getattr(user, currency) < price:
                return Response({"message": f"User does not have enough {currency}"}, status=400)

            # 扣除用户货币
            setattr(user, currency, getattr(user, currency) - price)
            user.save()

            # 记录用户的购买历史
            shoped_item, created = ShopedItem.objects.get_or_create(
                user_id=user_id,
                product_type=category,
                product_name=item_name,
                defaults={'quantity': 1}  # 仅在创建时设置默认的数量
            )

            if not created:
                # 如果用户已经购买过该商品，则增加购买数量
                shoped_item.quantity += 1
                shoped_item.save()

            # 发送购买信息到消息队列
            purchase_info = {
                'user_id': user_id,
                'item_name': item_name,
                'category': category,
                'price': price
            }
            channel.basic_publish(
                exchange='',
                routing_key='shop_purchase_queue',
                body=json.dumps(purchase_info)
            )

            # 使用 Celery 异步处理购买历史记录
            # process_purchase_history.delay(user_id, item_name, category)

            return Response({"message": "Successfully purchased item!"})

        finally:
            # 释放锁
            redis_instance.delete(lock_key)


# 确定货币类型
def determine_currency(category):
    diamond_categories = ['Time Acceleration Card', 'Food']
    return 'diamonds' if category in diamond_categories else 'coins'

from .models import ShopItem

class ShopListView(APIView):
    def get(self, request):
        # 查询所有ShopItem数据，并且用values()将其转换为字典列表形式
        items = ShopItem.objects.all().values('id', 'name', 'category', 'coins', 'diamonds')
        # 返回JSON数据给前端(或其他客户端)，safe=False是因为list不是字典
        return JsonResponse(list(items), safe=False)