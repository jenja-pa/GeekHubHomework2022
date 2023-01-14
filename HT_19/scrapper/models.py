from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class Products(models.Model):
    """
    Дані по продукту отриманому із rozetka_ip
    """
    item_id = models.CharField(max_length=30)
    title = models.CharField(max_length=130)
    old_price = models.FloatField() 
    current_price = models.FloatField()
    href = models.TextField()
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.title} : {self.current_price:.2f}"


# class Post(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(
#             default=timezone.now)
#     published_date = models.DateTimeField(
#             blank=True, null=True)

#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()

#     def __str__(self):
#         return self.title
