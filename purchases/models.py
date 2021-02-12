from decimal import Decimal
from django.db.models import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, DateField, DecimalField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey


class Customer(Model):
    name = CharField(max_length=200)
    address = CharField(max_length=200, blank=True)
    zip = CharField(max_length=10, blank=True)
    city = CharField(max_length=100, blank=True)
    email = CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Product(Model):
    description = CharField(max_length=200)
    category = CharField(max_length=50, blank=True)
    price = DecimalField(max_digits=7, decimal_places=2)
    active = BooleanField(default=True)

    def __str__(self):
        return self.description


class Invoice(Model):
    date = DateField()
    customer = ForeignKey(Customer, related_name='invoices', 
                            blank=False, on_delete=CASCADE)
    amount = DecimalField(max_digits=7, decimal_places=2)
    paymentdate = DateField(null=True, blank=True)
    paid = BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.customer, self.date)


class Purchase(Model):
    date = DateField()
    customer = ForeignKey(Customer, related_name='purchases', 
                            blank=False, on_delete=CASCADE)
    invoice = ForeignKey(Invoice, related_name='purchases',
                            blank=True, null=True, on_delete=CASCADE)

    @property
    def amount(self):
        sum = Decimal('0')
        for item in self.items.all():
            sum += item.amount
        return sum

    def __str__(self):
        return "%s - %s" % (self.customer, self.date)


class PurchaseItem(Model):
    purchase = ForeignKey(Purchase, related_name='items',
                            blank=False, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=PROTECT)
    price = DecimalField(max_digits=7, decimal_places=2)
    quantity = IntegerField()

    @property
    def amount(self):
        if self.quantity and self.price:
            return self.quantity * self.price
        return 0.0

    def clean(self):
        """
        model validation method.
        used to get the current price and store it
        in the item
        """
        if self.product:
            self.price = self.product.price

    
        





