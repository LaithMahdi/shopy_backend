from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=150)
    category_name_ar = models.CharField(max_length=150)
    category_picture = models.TextField()
    category_date = models.DateTimeField()

class Shoes(models.Model):
    shoes_name = models.CharField(max_length=255)
    shoes_name_ar = models.CharField(max_length=255)
    shoes_description = models.TextField()
    shoes_description_ar = models.TextField()
    shoes_picture = models.TextField()
    shoes_price = models.FloatField()
    shoes_discount = models.IntegerField(null=True,default=0)
    shoes_date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'shoes')