from django.db import models
import datetime

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'catogories'


    def __str__(self):
        return self.name

class customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1)
    description =models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to="upload/product")

    #Add more details about the sales

    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    
    
    def __str__(self):
        return self.name

    
  

class order(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product


