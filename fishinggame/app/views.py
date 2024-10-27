# Create your views here.
import hashlib
import time
import logging
import json
LOG = logging.getLogger(__name__)

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Achievement  # 确保导入了 User 模型


# Chat views
class ChatGeneralView(APIView):
    def post(self, request):
        # 在这里添加处理 general 聊天的逻辑
        return Response({"message": "General chat response"})


# Chat views
class ChatCommandView(APIView):
    def post(self, request):
        # 在这里添加处理 general 聊天的逻辑
        return Response({"message": "General chat response"})


# Chat views
class ChatDrawView(APIView):
    def post(self, request):
        # 在这里添加处理 general 聊天的逻辑
        return Response({"message": "General chat response"})


# Chat views
@csrf_exempt
def chat_general(request):
    return JsonResponse({"message": "General chat response"})

@csrf_exempt
def chat_command(request):
    return JsonResponse({"message": "Command response"})

@csrf_exempt
def chat_draw(request):
    return JsonResponse({"message": "Draw response"})


@csrf_exempt
def user_exist(request):
    user_id = request.GET.get('user_id')  # 从 GET 请求中获取 'user_id' 参数
    user = User.objects.filter(user_id=user_id).first()  # 查找用户是否存在

    if user:
        return JsonResponse({
            'code': 200,
            'msg': 'User exists',
            'data': {'exist': 1}
        })
    else:
        return JsonResponse({
            'code': 404,
            'msg': 'User not found',
            'data': {'exist': 0}
        })


@csrf_exempt
def user_create(request):
    LOG.info(f"【app.views.py -- user_create】：开始创建用户")
    try:
        data = json.loads(request.body)  # 解析 JSON 请求体
    except json.JSONDecodeError:
        return JsonResponse({'code': 400, 'msg': 'Invalid JSON'}, status=400)

    user_id = data.get('user_id')
    LOG.info(f"【app.views.py -- user_create】：获取到了user_id {user_id}")

    if not user_id:
        return JsonResponse({'code': 400, 'msg': 'parameter error'}, status=400)

    user_name = data.get('user_name')
    if User.objects.filter(user_id=user_id).exists():
        return JsonResponse({'code': 409, 'msg': 'already exist'}, status=409)

    User.objects.create(
        user_id=user_id,
        user_name=user_name,
        coins=0,
        diamonds=0,
        level=1,
        current_experience=0,
        experience_for_next_level=1,
        rod_type='Plastic Rod',
        fish_inventory=[]
    )
    return JsonResponse({'code': 201, 'msg': 'success'}, status=201)
#
# @csrf_exempt
# def user_create(request):
#     LOG.info(f"【app.views.py -- user_create】：开始创建用户{0}")
#     user_id = request.POST.get('user_id')
#     LOG.info(f"【app.views.py -- user_create】：获取到了user_id{user_id}")
#     print(user_id)
#     user_name = request.POST.get('user_name')
#     if not user_id:
#         return JsonResponse({'code': 400, 'msg': 'parameter error'}, status=400)
#     if User.objects.filter(user_id=user_id).exists():
#         return JsonResponse({'code': 409, 'msg': 'already exist'}, status=409)
#     User.objects.create(
#         user_id=user_id,
#         user_name=user_name,
#         coins=0,
#         diamonds=0,
#         level=1,
#         current_experience=0,
#         experience_for_next_level=1,
#         rod_type='Plastic Rod',
#         fish_inventory=[]
#     )
#     return JsonResponse({'code': 201, 'msg': 'success'}, status=201)


def generate_token(request):
    # 获取当前时间戳
    timestamp = str(int(time.time()))
    password = getattr(settings, 'API_PASSWORD', 'default_password')

    # 生成 token
    token = hashlib.md5(f"{password}{timestamp}{password}".encode()).hexdigest()

    return JsonResponse({
        'token': token,
        'timestamp': timestamp,
    })

@csrf_exempt
def user_basic(request):
    user_id = request.POST.get('user_id')
    if user_id:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            return JsonResponse({
                "user_id": user.user_id,
                "user_name": user.user_name,
                "rod_type": user.rod_type
            }, status=200)
        else:
            return JsonResponse({"message": "User not found"}, status=404)
    return JsonResponse({"message": "No user_id provided"}, status=400)


def user_finance(request):
    user_id = request.GET.get('user_id')
    if user_id:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            return JsonResponse({
                "coins": user.coins,
                "diamonds": user.diamonds
            }, status=200)
        else:
            return JsonResponse({"message": "User not found"}, status=404)
    return JsonResponse({"message": "No user_id provided"}, status=400)


def user_level(request):
    user_id = request.GET.get('user_id')
    if user_id:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            return JsonResponse({
                "level": user.level,
                "current_experience": user.current_experience,
                "experience_for_next_level": user.experience_for_next_level
            }, status=200)
        else:
            return JsonResponse({"message": "User not found"}, status=404)
    return JsonResponse({"message": "No user_id provided"}, status=400)


def user_inventory(request):
    user_id = request.GET.get('user_id')
    if user_id:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            return JsonResponse({
                "fish_inventory": user.fish_inventory
            }, status=200)
        else:
            return JsonResponse({"message": "User not found"}, status=404)
    return JsonResponse({"message": "No user_id provided"}, status=400)


def user_achievement(request):
    user_id = request.GET.get('user_id')
    if user_id:
        user = User.objects.filter(user_id=user_id).first()
        if user:
            achievements = Achievement.objects.filter(user=user).values('user', 'type', 'weight')
            return JsonResponse({
                "achievements": list(achievements)
            }, status=200)
        else:
            return JsonResponse({"message": "User not found"}, status=404)
    return JsonResponse({"message": "No user_id provided"}, status=400)

# Fish views
@csrf_exempt
def fish_catch(request):
    return JsonResponse({"message": "Fish caught"})

@csrf_exempt
def fish_sell(request):
    return JsonResponse({"message": "Fish sold"})

# Shop views
def shop_list(request):
    return JsonResponse({"message": "Shop item list"})

@csrf_exempt
def shop_purchase(request):
    return JsonResponse({"message": "Item purchased"})