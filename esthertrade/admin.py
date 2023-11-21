from django.contrib import admin
from .models import Commodity,Order,OrderItem
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    pass

# Define a custom admin class for Commodity
@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('image','name', 'price')
    list_filter = ('name',)  # Add more filters as needed
    search_fields = ('name',)  # Add more search fields as needed
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_no', 'ordered_at', 'delivery_fee', 'delivery_place', 'total_amount', 'formatted_commodities']

    def formatted_commodities(self, obj):
        items = obj.items.all()
        item_list = [str(item) for item in items]
        return format_html(", ".join(item_list))
    formatted_commodities.short_description = 'Items'

class OrderItemAdmin(admin.ModelAdmin):
    list_display =['order','commodity','quantity','item_price']
admin.site.register(Order, OrderAdmin),
admin.site.register(OrderItem, OrderItemAdmin)
# Register your models here.
