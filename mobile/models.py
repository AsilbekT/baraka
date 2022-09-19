from django.db import models
from django.conf import settings
from accounts.models import Account, Customer

class MainCatagory(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="catagories", default="default.jpg")
    
    def __str__(self):
        return self.name


class Catagory(models.Model):
    main_catagory = models.ForeignKey(MainCatagory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs): # new
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Product(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    catagory_name = models.CharField(max_length=100, blank=True, default='do not enter')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    narx = models.IntegerField(default=0)
    image = models.ImageField(upload_to ='products/', default="default.jpg")
    availa = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    liked = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.checked == False:
            self.catagory_name = self.catagory.name
            self.checked = True
        super(Product, self).save(*args, **kwargs)

    @property
    def get_absolute_image_url(self):
        return "{}{}".format(settings.MEDIA_URL, self.image.url)

    def __str__(self):
        return self.name



        
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, default='Tashkent')
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total


    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_ended = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True,  on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True,  on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address