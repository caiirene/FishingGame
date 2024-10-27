from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # 用户ID
    user_name = models.CharField(max_length=255)  # 用户名
    coins = models.IntegerField(default=0)  # 用户金币数量
    diamonds = models.IntegerField(default=0)  # 用户钻石数量
    level = models.IntegerField(default=1)  # 用户等级
    current_experience = models.IntegerField(default=0)  # 当前经验值
    experience_for_next_level = models.IntegerField(default=100)  # 升级所需经验值
    rod_type = models.CharField(max_length=255, default='basic')  # 钓鱼竿类型
    fish_inventory = models.JSONField(default=list)  # 鱼类库存（可以存储为JSON）

    def __str__(self):
        return self.user_name


class User(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # 用户ID
    user_name = models.CharField(max_length=255)  # 用户名
    coins = models.IntegerField(default=0)  # 用户金币数量
    diamonds = models.IntegerField(default=0)  # 用户钻石数量
    level = models.IntegerField(default=1)  # 用户等级
    current_experience = models.IntegerField(default=0)  # 当前经验值
    experience_for_next_level = models.IntegerField(default=100)  # 升级所需经验值
    rod_type = models.CharField(max_length=255, default='basic')  # 钓鱼竿类型
    fish_inventory = models.JSONField(default=list)  # 鱼类库存（可以存储为JSON）

    def __str__(self):
        return self.user_name


class Fish(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()
    probability = models.FloatField()
    status = models.BooleanField(default=True)
    s_weight = models.FloatField(null=True, blank=True)
    a_weight = models.FloatField(null=True, blank=True)
    b_weight = models.FloatField(null=True, blank=True)
    c_weight = models.FloatField(null=True, blank=True)
    mean = models.FloatField(default=1.75)
    standard_deviation = models.FloatField(default=0.625)


class FishCatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fish_type = models.ForeignKey(Fish, on_delete=models.CASCADE)
    weight = models.FloatField()
    rarity_level = models.CharField(max_length=50)
    image_url = models.URLField()
    caught_at = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fish_catched = models.ManyToManyField(FishCatched)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    weight = models.FloatField()
