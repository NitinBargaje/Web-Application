from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products')
    description = models.CharField(
        max_length=200, default='', null=True, blank=True)

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category(category_id):
        return Product.objects.filter(category=category_id)

    
class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False

    def register(self):
        self.save()
