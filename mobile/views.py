from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from mobile.models import Catagory, Product, Customer, Order, OrderItem
from mobile.serializers import CatagorySerializer, ProductSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET', 'POST'])
def catagory_list(request):
    """
    List all code catagorys, or create a new catagory.
    """
    if request.method == 'GET':
        catagory = Catagory.objects.all()
        serializer = CatagorySerializer(catagory, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CatagorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all code catagorys, or create a new catagory.
    """
    if request.method == 'GET':
        # product_objects = cache.get('products')      # NEW
        product_objects = Product.objects.all()

            # cache.set('products', product_objects)  
        serializer = ProductSerializer(product_objects, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@api_view(['POST'])
def store(request):
    if request.method == "POST":
        got_token = request.data['token']
        token = Token.objects.get(key=got_token)
        user = token.user
        customer = Customer.objects.get(user=user)
        try:
            product = Product.objects.get(id=request.data['product_id'])
            order, created  = Order.objects.get_or_create(customer=customer, complete=False)
            if int(product.available) >= int(request.data['quantity']):
                orderItems = OrderItem.objects.create(order=order, product=product, quantity=request.data['quantity'])
                product.available -= int(request.data['quantity'])
                product.save()
            elif int(product.available) < int(request.data['quantity']):
                return Response({"status":"omborda yetarli maxsulot yo'q"})
            
        except:
            return Response({"status":"xatolik bor"})
    return Response({"status":"Muvaffaqiyatli saqlandi"})


@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        product_detail_json = ProductSerializer(product)
        return Response(product_detail_json.data, status=201)

    except ObjectDoesNotExist:
        return Response({"error": "Bu maxsulot yo'q"})

    return Response({"status":"Muvaffaqiyatli saqlandi"})