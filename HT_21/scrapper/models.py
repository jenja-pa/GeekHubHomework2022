from django.db import models


# Create your models here.
class Category(models.Model):
    """
    Категорії продуктів - пов'язана модель
    """
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Дані по продукту отриманому із rozetka_ip
    """
    item_id = models.CharField(max_length=30)
    title = models.CharField(max_length=130)
    sell_status = models.CharField(max_length=12, default='available')
    old_price = models.FloatField()
    current_price = models.FloatField()
    href = models.TextField()
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    url_image_preview = models.TextField(null=True)
    url_image_big = models.TextField(null=True)

    def __str__(self):
        # print(f"---{dir(self)=}")
        return (f"{self.title} : {self.current_price:.2f} : "
                f"{self.category} : "
                f"{self.str_available}")

    @property
    def is_available(self):
        return self.sell_status == 'available'

    @property
    def str_available(self):
        if self.is_available:
            return 'В наявності'
        else:
            return 'Відсутній'


# на видалення
class BackgroundProcessMessage(models.Model):
    """
    Тимчасове повідомлення від фонового
    процесу про його виконання
    """
    value = models.TextField()
