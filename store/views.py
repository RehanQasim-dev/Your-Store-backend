
from urllib import request
from django.http import HttpRequest
from requests import delete
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from .models import CartItem, Product, Review
from .serializers import *
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAdminOrAuthPOST, IsAdminOrAuthRead, IsAdminOrReadOnly
class ViewSetProduct(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields=['collection_id',ProductFilter]
    filterset_class=ProductFilter
    search_fields=["title"]
    ordering_fields=['last_update','price']
    permission_classes=[IsAdminOrReadOnly]
    def get_queryset(self):
        collect_id=self.request.query_params.get("collection_id")
        if collect_id is not None:
            return Product.objects.filter(collection_id=collect_id)
        return Product.objects.all()
    def destroy(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0 or product.cartitem_set.count()>0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ViewSetCollection(ModelViewSet):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer
    permission_classes=[IsAdminOrReadOnly]
    def destroy(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.product_set.count()>0:
            return Response(data={'error':"cant delete"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class ViewSetCart(ModelViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer
    def destroy(self,request,pk):#remember self parameter
        cart=get_object_or_404(Cart,id=pk)
        if cart.items.count()>0:
            return Response(data={'error':"cant delete"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

class ViewSetCartItem(ModelViewSet):
    http_method_names=['get','post','patch','delete'] #all should be in lowercase
    serializer_class=CartItemSerializer         #here
    def get_serializer_class(self):
        if self.request.method=='GET':
            return CartItemSerializer
        elif self.request.method=='POST':
            return CartItemCreateSerializer
        else :
            return CartItemUpdateSerializer
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
# class ViewSetCustomer(ModelViewSet):
#     queryset=Customer.objects.all()
#     permission_classes=[IsAuthenticated]
#     def get_serializer_class(self):
#         if self.action=='me':
#             return CustomerSerializer_me
#         return CustomerSerializer
#     @action(detail=False,methods=['GET',"PATCH"],permission_classes=[IsAuthenticated])
#     def me(self,request:HttpRequest):
#         # if request.user.is_anonymous:
#         #     return Response('Your are not Authenticated')
#         _id=request.user.id
#         (instant,bol)=Customer.objects.get_or_create(user_id=_id)
#         if request.method=='GET':
#             serializer=CustomerSerializer(instant)#serializer takes object or queryset
#             return Response(serializer.data)
#         elif request.method=="PATCH":
#             print(request.data)
#             serializer=CustomerSerializer(instant,data=request.data,partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)

class ViewSetOrder(ModelViewSet):
    http_method_names=['post','get','patch','delete']
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
    def get_queryset(self):
        customer=Customer.objects.get(user_id=self.request.user.id)
        if self.request.user.is_staff:
            return Order.objects.all()
        '''so while accessing detail given a order_id of the order
        it will return data if the id is included in the return query set
        not in our database'''
        return Order.objects.filter(customer_id=customer.id)

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_serializer_class(self):
        '''if self.request.method=="GET" or "DELETE"#this syntax is not correct'''
        if self.request.method in ['PUT','PATCH']:
            return OrderSerializerUpdate
        else:
            return OrderSerializer
                                    #it will try to use this for delete also
                                    #as cart _id is not a valid field it can only
                                #be used in put post patch without error but when this serializer will be
                                #for shwoing data u will
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        element=serializer.save()
        serializer=OrderSerializer(instance=element)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class ViewSetCustomer(ModelViewSet):
    serializer_class=CustomerSerializer
    def get_queryset(self):
        if self.request.method=='GET':
            user=self.request.user
            customer=get_object_or_404(Customer,user__id=user.id)
            return customer
        else:
            return Customer
    def create(self, request, *args, **kwargs):
        if Customer.objects.filter(user__id=request.data['user']).exists():
            return Response('Customer Already Registered with this user id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance=self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class ViewSetOrderItem(ModelViewSet):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    permission_classes =[IsAdminOrAuthRead]
class ViewSetProductImage(ModelViewSet):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer
    def get_serializer_context(self):
        return {'product_id':self.kwargs['Product_pk']}
    # def get_permissions(self):
    #     if self.request.method=='GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
class ViewSetReview(ModelViewSet):
    serializer_class=ReviewSerializer
    queryset=Review.objects.all()
    permission_classes=[IsAuthenticated]
    def get_serializer_context(self):
        return {'user_id':self.request.user.id,'product_id':self.kwargs['Product_pk']}
# class ProductList(ListCreateAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     def get_serializer_context(self):
#         return {"request",self.request}
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     def delete(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         if product.orderitem_set.count()>0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
 
# class CollectionList(ListCreateAPIView):
#     queryset=Collection.objects.all()
#     serializer_class=CollectionSerializer
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Collection.objects.all()
#     serializer_class=CollectionSerializer
#     def  delete(request,pk):
#         collection=get_object_or_404(Collection,pk=pk)
#         if collection.product_set.count()>0:
#             return Response(data={'error':"cant delete"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































    