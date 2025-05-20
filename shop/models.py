from django.db import models
from decimal import Decimal
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = ['my_order']



class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null = True, blank = True )
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to = 'products/')
    discount = models.PositiveIntegerField(default = 0)
    category = models.ForeignKey(Category, related_name='products', on_delete= models.SET_NULL, null = True, blank = True)
    amount = models.PositiveIntegerField(default = 0)


    def __str__(self):
        return self.name


    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * Decimal(f'{1 - (self.discount / 100)}')
        return self.price

    @property
    def get_absolute_url(self):
        if self.image:
            return self.image.url
        return ''

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering = ['my_order']


class Order(BaseModel):
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default = 0)
    product = models.ForeignKey(Product, related_name='orders', on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f'{self.name} - {self.quantity}'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=250)
    email = models.EmailField()
    content = models.TextField()
    product = models.ForeignKey(Product, related_name='comments', on_delete = models.CASCADE )
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.THREE.value )

    def __str__(self):
        return f'{self.name} - {self.rating}'


