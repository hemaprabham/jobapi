# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.serializers import ValidationError



#vendors
@csrf_exempt
def addall(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        print(received_data)
        
        
        serializer_check = VendorSerializer(data=received_data)
        
        if serializer_check.is_valid():
            serializer_check.save()
            return HttpResponse(json.dumps({"status": "success"}))
        else:
            return HttpResponse(json.dumps({"status": "failed"}))    

@api_view(['GET'])
def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def retrieve_vendor(request, vendor_id):
    try:
        vendor = get_object_or_404(Vendor, vid=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": f"Vendor with id {vendor_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    return JsonResponse({"status": "Invalid Request Method"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def update_vendor_details(request):
    if request.method == "PUT":
        received_data = json.loads(request.body)
        vendor_id = received_data.get("vid")
        vendor_name = received_data.get("name")
        contact_details = received_data.get("contact_details")
        address = received_data.get("address")
        vendor_code = received_data.get("vendor_code")
        on_time_delivery_rate = received_data.get("on_time_delivery_rate", 0.0)
        quality_rating_avg = received_data.get("quality_rating_avg", 0.0)
        average_response_time = received_data.get("average_response_time", 0.0)
        fulfillment_rate = received_data.get("fulfillment_rate", 0.0)

        if not all([vendor_id, vendor_name, contact_details, address, vendor_code]):
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            vendor = Vendor.objects.get(vid=vendor_id)
            vendor.name = vendor_name
            vendor.contact_details = contact_details
            vendor.address = address
            vendor.vendor_code = vendor_code
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.quality_rating_avg = quality_rating_avg
            vendor.average_response_time = average_response_time
            vendor.fulfillment_rate = fulfillment_rate

            vendor.save()
            return JsonResponse({"status": "Updated successfully"})
        except Vendor.DoesNotExist:
            return JsonResponse({"status": f"Vendor with id {vendor_id} not found"}, status=404)

    return JsonResponse({"status": "Invalid Request Method"}, status=400)

@csrf_exempt
def delete_vendor_details(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        vendor_id = received_data.get("vid")
        
        if not vendor_id:
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            vendor = Vendor.objects.get(vid=vendor_id)
            vendor.delete()
            return HttpResponse(json.dumps({"status": "Deleted Successfully"}))
        except Vendor.DoesNotExist:
            return HttpResponse(json.dumps({"status": f"Vendor with id {vendor_id} not found"}))
            
    return JsonResponse({"status": "Invalid Request Method"}, status=400)    

#purchase   
@csrf_exempt
def add_purchase_order(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        serializer_check = PurchaseOrderSerializer(data=received_data)
        
        try:
            serializer_check.is_valid(raise_exception=True)
            serializer_check.save()
            return HttpResponse(json.dumps({"status": "purchase addedd success"}))
        except ValidationError as e:
            return HttpResponse(json.dumps({"status": "purchase adding failed", "errors": e.detail}), status=400)

@api_view(['GET'])
def list_purchase_orders(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def retrieve_purchase_order(request, po_id):
    try:
        purchase_order = get_object_or_404(PurchaseOrder, pid=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": f"PurchaseOrder with id {po_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    return JsonResponse({"status": "Invalid Request Method"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def update_purchase_order_details(request):
    if request.method == "PUT":
        received_data = json.loads(request.body)
        po_id = received_data.get("pid")

        if not po_id:
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            purchase_order = PurchaseOrder.objects.get(pid=po_id)
            serializer = PurchaseOrderSerializer(purchase_order, data=received_data)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "purchase Updated successfully"})
            else:
                return JsonResponse({"status": "Invalid input data"}, status=400)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({"status": f"PurchaseOrder with id {po_id} not found"}, status=404)

    return JsonResponse({"status": "Invalid Request Method"}, status=400)

@csrf_exempt
def delete_purchase_order_details(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        po_id = received_data.get("pid")

        if not po_id:
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            purchase_order = PurchaseOrder.objects.get(pid=po_id)
            purchase_order.delete()
            return HttpResponse(json.dumps({"status": "purchase Deleted Successfully"}))
        except PurchaseOrder.DoesNotExist:
            return HttpResponse(json.dumps({"status": f"PurchaseOrder with id {po_id} not found"}))

    return JsonResponse({"status": "Invalid Request Method"}, status=400)

#order
@csrf_exempt
def add_historical_performance(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        serializer_check = HistoricalPerformanceSerializer(data=received_data)

        try:
            serializer_check.is_valid(raise_exception=True)
            serializer_check.save()
            return HttpResponse(json.dumps({"status": "historical performance added successfully"}))
        except ValidationError as e:
            return HttpResponse(json.dumps({"status": "historical performance adding failed", "errors": e.detail}), status=400)
@api_view(['GET'])
def list_historical_performances(request):
    if request.method == 'GET':
        historical_performances = HistoricalPerformance.objects.all()
        serializer = HistoricalPerformanceSerializer(historical_performances, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def retrieve_historical_performance(request, hid):
    try:
        historical_performance = get_object_or_404(HistoricalPerformance, hid=hid)
    except HistoricalPerformance.DoesNotExist:
        return Response({"error": f"HistoricalPerformance with id {hid} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HistoricalPerformanceSerializer(historical_performance)
        return Response(serializer.data)

    return JsonResponse({"status": "Invalid Request Method"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def update_historical_performance_details(request):
    if request.method == "PUT":
        received_data = json.loads(request.body)
        hid = received_data.get("hid")

        if not hid:
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            historical_performance = HistoricalPerformance.objects.get(hid=hid)
            serializer = HistoricalPerformanceSerializer(historical_performance, data=received_data)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "order Updated successfully"})
            else:
                return JsonResponse({"status": "Invalid input data"}, status=400)
        except HistoricalPerformance.DoesNotExist:
            return JsonResponse({"status": f"HistoricalPerformance with id {hid} not found"}, status=404)

    return JsonResponse({"status": "Invalid Request Method"}, status=400)

@csrf_exempt
def delete_historical_performance_details(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        hid = received_data.get("hid")

        if not hid:
            return JsonResponse({"status": "Invalid input data"}, status=400)

        try:
            historical_performance = HistoricalPerformance.objects.get(hid=hid)
            historical_performance.delete()
            return HttpResponse(json.dumps({"status": "order Deleted Successfully"}))
        except HistoricalPerformance.DoesNotExist:
            return HttpResponse(json.dumps({"status": f"HistoricalPerformance with id {hid} not found"}))

    return JsonResponse({"status": "Invalid Request Method"}, status=400)

 
