from django.shortcuts import render
from rest_framework.views import APIView
from core import serializers,models
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


class ProductApiView(APIView):
    model_class = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self,request,pk=None):
        if pk:
            try:
                product = models.Product.objects.get(pk=pk)
            except:
                return Response(
                    {
                        'message':'this product you are looking for is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )  
            serializer = serializers.ProductSerializer(product)  
            return Response(serializer.data)
        else:
            product = models.Product.objects.all()
            serializer = serializers.ProductSerializer(product, many=True)
            return Response(serializer.data)
        

    def post(self,request,pk=None):
        serializer = self.serializer_class(data=request.data)
        if pk:
            return Response(
                {
                    'message':'this process is not available'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
           if serializer.is_valid():
               user_model=get_user_model()
               user=user_model.objects.get(email=request.user.email)
               serializer.validated_data['created_by']=user
               serializer.save()
               return Response(
                   {
                       'message':'categoty created successfully',
                       'the new category': serializer.data
                   },
                   status=status.HTTP_201_CREATED
               )
           else:
               return Response(
                   {
                       'message':'ur object is not valid',
                       'errors': serializer.errors
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        
        



class CategoryApiView(APIView):
    model_class = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self,request,pk=None):
        if pk:
            try:
                category=models.Category.objects.get(pk=pk)
            except:
                return Response(
                    {
                        'message':'not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer=serializers.CategorySerializer(category) 
            return Response(serializer.data)  

        else:
            category=models.Category.objects.all()
            serializer=serializers.CategorySerializer(category,many=True)  #many=True
            return Response(serializer.data) 
        

    def post(self,request,pk=None):
        serializer = self.serializer_class(data=request.data)
        if pk:
            return Response(
                {
                    'message':'this process is not available'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
           if serializer.is_valid():
               serializer.save()
               return Response(
                   {
                       'message':'categoty created successfully',
                       'the new category': serializer.data
                   },
                   status=status.HTTP_201_CREATED
               )
           else:
               return Response(
                   {
                       'message':'ur object is not valid',
                       'errors': serializer.errors
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )  


class OrderApiView(APIView):
    model_class = models.Order.objects.all() 
    serializer_class = serializers.OrderSerializer

    def get(self,request,pk=None):
        order=models.Order.objects.all()
        serializer=serializers.OrderSerializer(order,many=True) 
        return Response(serializer.data)  

    def post(self,request,pk=None):
        serializer=serializers.OrderSerializer(data=request.data)  
        if pk:
            return Response(
                {
                    'message':'u cant do this process'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:           
            if serializer.is_valid():
                user_model=get_user_model()
                user=user_model.objects.get(email=request.user.email)
                serializer.validated_data['order_by']=user
                serializer.save()
                return Response(
                    {
                        'message':'order created successfully',
                        'data':serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'message':'cant create order',
                        'error':serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )