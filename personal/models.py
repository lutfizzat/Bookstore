# from django.db import models
# from django.db.models.fields import BooleanField, DateTimeField
# from account.models import Account

# class Buyer(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     price = models.FloatField()
#     digital = models.BooleanField(default=False, null=True, blank=False)
#     #image

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, blank=True, null=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=False)
#     transaction_id = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return str(self.id)

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)

# class ShippingAddress(models.Model):
#     buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, blank=True, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True, null=True)
#     address = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=200, null=True)
#     state = models.CharField(max_length=200, null=True)
#     zipcode = models.CharField(max_length=200, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address


