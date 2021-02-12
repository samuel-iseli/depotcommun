import datetime
from django.contrib import admin
from django.contrib import admin

from .models import Customer, Product, Purchase, PurchaseItem, Invoice

def create_invoice(modeladmin, request, queryset):
    for purchase in queryset.all():
        if purchase.invoice:
            continue    

        inv = Invoice.objects.create(
                date=datetime.date.today(),
                customer=purchase.customer,
                amount=purchase.amount
                )
        purchase.invoice = inv
        inv.save()
        purchase.save()

create_invoice.short_description = "Create invoice"



class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    readonly_fields = ('price', 'amount')
    fields = ('product', 'quantity', 'price', 'amount')
    extra = 1

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'invoice')
    fields = (('customer', 'date'), 'invoice' )
    inlines = (PurchaseItemInline, )
    actions = (create_invoice, )


# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Invoice)
