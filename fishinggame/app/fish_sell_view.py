from django.db import transaction
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F


from app.models import Inventory, FishCatched, User


class FishSellView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')

            # 检查是否有库存记录
            inventory_exists = Inventory.objects.filter(user_id=user_id).exists()
            if not inventory_exists:
                return Response({'revenue': 0}, status=200)

            # 计算利润
            total_value = Inventory.objects.filter(user_id=user_id).aggregate(
                total_value=Sum(F('weight') * F('price'))
            )['total_value'] or 0

            # 使用事务确保数据一致性
            with transaction.atomic():
                # 释放库存中的鱼
                FishCatched.objects.filter(inventory__user_id=user_id).delete()

                # 增加账户余额
                User.objects.filter(id=user_id).update(coins=F('coins') + total_value)
            return Response({'revenue': total_value}, status=200)
        except Exception as e:
            return Response({'message': 'failed'}, status=500)
