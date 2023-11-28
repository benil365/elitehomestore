from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import  CommodityForm, OrderForm
from .models import Order, OrderItem, Commodity
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from decimal import Decimal  
from collections import Counter
# Create your views here.
class Homepage(TemplateView):
    template_name="home.html"
class OrderPage(TemplateView):
    template_name ="order.html"
class SubmitOrder(TemplateView):
    template_name ="success.html"


class CommodityView(View):
    template_name = "home.html"

    def get(self, request):
        form = CommodityForm()
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        form = CommodityForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Commodity submitted successfully!')
            # Redirect to another view or URL
            return redirect("item")
        else:
            messages.error(request, 'Error in the form submission. Please correct the errors.')

        # If the form is not valid, re-render the template with the form and error messages
        return render(request, self.template_name, {"form": form})

def order_view(request):
    orders = Order.objects.all()
    orders = Order.objects.order_by('-ordered_at')
    # Iterate through each order and fetch its associated order items
    for order in orders:
        order.order_items = order.orderitem_set.all()

    context = {
        'orders': orders,
    }
    return render(request, 'order.html', context)

def home_view(request):
    commodities = Commodity.objects.all()
    order_items = OrderItem.objects.all()  # Get all order items
    return render(request, 'home.html', {'commodities': commodities, 'order_items': order_items})


def get_item_by_name(item_name):
    try:
        return OrderItem.objects.get(pk=item_name)
    except OrderItem.DoesNotExist:
        
        return None  

def select_items(request, item_name):
    # Check if there's a list of selected items in the session
    commodity = get_object_or_404(Commodity, name=item_name)
    selected_items = request.session.get('selected_items', [])
    selected_items.append(commodity.id)
    request.session['selected_items'] = selected_items
    # Render the page where the user selects items
    messages.success(request, f"Successfully added {commodity.name} to the cart.")

    return redirect('home')


def create_order(request):
    selected_items_ids = request.session.get('selected_items', [])
    selected_items = Commodity.objects.filter(id__in=selected_items_ids)
    total_price = sum(Decimal(item.price) for item in selected_items)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order(
                    email=form.cleaned_data['email'],
                    phone_no=form.cleaned_data['phone_no'],
                    delivery_place=form.cleaned_data['delivery_place'],
                    delivery_fee=Decimal()  # Convert delivery_fee to Decimal
                )
                order.save()
                selected_items_counter = Counter(selected_items_ids)

                for commodity in selected_items:
                    quantity = selected_items_counter[commodity.id]
                    item_price = Decimal(commodity.price)  # Convert item.price to Decimal

                    order_item = OrderItem(
                        commodity=commodity,
                        order=order,
                        quantity=quantity,
                        item_price=item_price
                    )
                    order_item.save()
                    total_price += quantity * item_price
                order.total_amount = total_price
                order.save()
                del request.session['selected_items']
                messages.success(request, f"{commodity.name} was successfully added to your cart.")
                return render(request, 'success.html', {'order': order, 'total_price': order.total_amount})
    else:
        form = OrderForm()
    return render(request, 'order.html', {'selected_items': selected_items, 'total_price': total_price, 'form': form})

def remove_selected_item(request, item_name):
    commodity = get_object_or_404(Commodity, name=item_name)
    selected_items = request.session.get('selected_items', [])
    
    # Remove the commodity ID from selected_items instead of its name
    selected_items = [item_id for item_id in selected_items if item_id != commodity.id]
    
    request.session['selected_items'] = selected_items
    request.session.modified = True
    
    # Redirect back to the page where items are displayed (e.g., home_view or any relevant view)
    return redirect('home')  # Adjust this redirection as per your application flow

  


   




