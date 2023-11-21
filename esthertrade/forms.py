from django import forms
from .models import Commodity,Order,OrderItem

class CommodityForm(forms.ModelForm):
    class Meta:
       model = Commodity
       fields =['name','image','category','description','price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['ordered_at'] 
        fields = ['email','phone_no','delivery_fee','delivery_place']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields =['order','commodity','quantity','item_price']
