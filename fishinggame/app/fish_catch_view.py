from rest_framework.views import APIView
from rest_framework.response import Response
import random
import math
from .models import Fish, Inventory, FishImages


class FishCatchView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        fish_list = Fish.objects.filter(status='1').values()

        fish_chosen = self.probability_helper(fish_list)
        weight = self.weight_generator(fish_chosen)

        # 图片生成部分，暂时返回一个写死的图片URL
        img_url = self.image_helper(weight, fish_chosen)

        Inventory.objects.create(
            user_id=user_id,
            type=fish_chosen['type'],
            price=1,
            weight=weight,
            url=img_url,
            description=fish_chosen['description']
        )

        return Response({
            'type': fish_chosen['type'],
            'weight': weight,
            'description': fish_chosen['description'],
            'url': img_url,
            'status': 'Successfully Caught!'
        })

    def probability_helper(self, fish_list):
        total_probability = sum(fish['probability'] for fish in fish_list)
        random_probability = random.random() * total_probability
        current_prob = 0
        for fish in fish_list:
            current_prob += fish['probability']
            if current_prob > random_probability:
                return fish
        return fish_list[-1]

    def weight_generator(self, fish):
        mean = fish.get('mean', 1.75)
        standard_deviation = fish.get('standard_deviation', 0.625)
        u1 = random.random()
        u2 = random.random()
        rand_std_normal = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        return mean + standard_deviation * rand_std_normal

    def image_helper(self, weight, fish_chosen):
        # 图片URL逻辑暂时写死为一个默认值
        default_img_url = 'https://s3.us-west-1.amazonaws.com/fishing.web.images/Fishing+Game+Images/Other/pearl.png'

        fish_img = FishImages.objects.filter(type=fish_chosen['type']).first()

        if fish_img and fish_img.images:
            score = self.evaluate(weight, fish_chosen)
            images = fish_img.images

            if images.get(score) and images[score][0].get('url'):
                return images[score][0]['url']

        return default_img_url

    def evaluate(self, weight, fish_chosen):
        s_weight = fish_chosen.get('s_weight', 20)
        a_weight = fish_chosen.get('a_weight', 19)
        b_weight = fish_chosen.get('b_weight', 18)
        c_weight = fish_chosen.get('c_weight', 17)

        if weight > s_weight:
            return 'SS'
        elif weight > a_weight:
            return 'S'
        elif weight > b_weight:
            return 'A'
        elif weight > c_weight:
            return 'B'
        else:
            return 'C'
