from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import SubmitOrder, create_order,order_view,home_view, select_items, remove_selected_item

urlpatterns = [
    path('', home_view, name='home'),
    path('add_item/<str:item_name>/', select_items, name='add_item'),
    path('remove_item/<str:item_name>/', remove_selected_item, name='remove_item'), 
    path("success", SubmitOrder.as_view(), name="success"),
    path("details/",create_order, name="order_details"),
    path('orders/', order_view, name='order_view'),
    # Other URL patterns for your app...
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)