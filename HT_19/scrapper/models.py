from django.db import models


# Create your models here.
class Product(models.Model):
    """
    Дані по продукту отриманому із rozetka_ip
    """
    item_id = models.CharField(max_length=30)
    title = models.CharField(max_length=130)
    old_price = models.FloatField()
    current_price = models.FloatField()
    href = models.TextField()
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=30)
    url_image_preview = models.TextField(null=True)
    url_image_big = models.TextField(null=True)

    def __str__(self):
        return f"{self.title} : {self.current_price:.2f}"


class BackgroundProcessMessage(models.Model):
    """
    Тимчасове повідомлення від фонового
    процесу про його виконання
    """
    value = models.TextField()
