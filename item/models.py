from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True,
        validators=[
            MaxValueValidator(99999, message="Price cannot exceed 5 digits."),
            MinValueValidator(-10000, message="Price cannot be negative.")
        ]
    )
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PriceRange(models.Model):
    name = models.CharField(max_length=255)
    min_price = models.FloatField()
    max_price = models.FloatField()

    def __str__(self):
        return self.name
