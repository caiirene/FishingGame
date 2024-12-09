from django.contrib.sites import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fishinggame import settings


class ChatGeneralView(APIView):
    def post(self, request):
        try:
            api_key = settings.OPENAI_API_KEY
            user_message = request.data.get('message')

            if not user_message:
                return Response({"message": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

            # OpenAI API 请求的参数
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': user_message}
                ]
            }

            # 发送 POST 请求到 OpenAI API
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

            # 解析响应
            if response.status_code == 200:
                result = response.json()
                filtered_result = result['choices'][0]['message']['content'] if result.get('choices') else 'No content'
                return Response({"message": filtered_result}, status=200)
            else:
                return Response({"message": "Failed to get a response from OpenAI"}, status=response.status_code)

        except Exception as e:
            # 处理可能的异常并记录错误信息
            return Response({"message": "Internal server error"}, status=500)



class ChatCommandView(APIView):
    def post(self, request):
        try:
            api_key = settings.OPENAI_API_KEY  # 从 Django 的 settings 中获取 OpenAI API 密钥

            message = request.data.get('message')
            key_words = ['fish', 'play', 'sell']

            key_words_str = ','.join(key_words)

            prompt = f'Given the keywords [{key_words_str}], please match them to the message: "{message}" and return the matched keywords. And return the closest matched keyword. Cannot return none. Just return the keyword without any description!'

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are going to identify the keywords in a given sentence'},
                    {'role': 'user', 'content': prompt}
                ]
            }

            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                filtered_result = result['choices'][0]['message']['content'].strip() if result.get('choices') else 'No content'
                return Response({'keyword': filtered_result}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to get a response from OpenAI'}, status=response.status_code)

        except Exception as e:
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatDrawView(APIView):
    def post(self, request):
        try:
            api_key = settings.OPENAI_API_KEY  # 从 settings 文件中获取 OpenAI API 密钥

            prompt = request.data.get('prompt')

            # 检查 prompt 是否存在
            if not prompt:
                return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

            # 根据样例构建详细的 prompt
            detailed_prompt = f"Given the keywords [{prompt}], draw an image that relates to the keywords - requirements: Note: the image created should be more realistic, rather than in cartoon style."

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
            data = {
                'prompt': detailed_prompt,
                'n': 1,
                'size': '1024x1024'
            }

            response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                image_url = result.get('data', [])[0].get('url', 'No content')
                return Response({'image_url': image_url}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to generate image'}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

