# urls.py

from django.urls import path
from .import views

urlpatterns = [
    path('listvendors/', views.list_vendors, name='list-vendors'),
    path('<int:vendor_id>/', views.retrieve_vendor, name='retrieve-vendor'),
    path('', views.addall, name='addall'),
    path('vendors/update/',views.update_vendor_details, name='update_vendor_details'),
    path('vendors/delete/',views.delete_vendor_details, name='delete_vendor_details'),
    #purchase
    path('add_purchase_order/', views.add_purchase_order, name='add_purchase_order'),
    path('list_purchase_orders/',views. list_purchase_orders, name='list_purchase_orders'),
    path('retrieve_purchase_order/<int:po_id>/', views.retrieve_purchase_order, name='retrieve_purchase_order'),
    path('update_purchase_order_details/',views. update_purchase_order_details, name='update_purchase_order_details'),
    path('delete_purchase_order_details/',views. delete_purchase_order_details, name='delete_purchase_order_details'),
    #orders
    path('add_historical_performance/',views. add_historical_performance, name='add_historical_performance'),
    path('list_historical_performances/', views.list_historical_performances, name='list_historical_performances'),
    path('retrieve_historical_performance/<int:hid>/', views.retrieve_historical_performance, name='retrieve_historical_performance'),
    path('update_historical_performance_details/',views. update_historical_performance_details, name='update_historical_performance_details'),
    path('delete_historical_performance_details/',views. delete_historical_performance_details, name='delete_historical_performance_details'),


]
