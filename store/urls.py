from django.urls import path
from . import views
from rest_framework_nested import routers
router=routers.DefaultRouter()
router.register("Products",views.ViewSetProduct,basename="ello1")
router.register("Collections",views.ViewSetCollection,basename="ello2")
router.register("Carts",views.ViewSetCart,basename="ello3")
router.register("Customers",views.ViewSetCustomer,basename='customer')
router.register("Orders",views.ViewSetOrder)
nested1=routers.NestedDefaultRouter(parent_router=router,parent_prefix="Products",lookup="Product")
nested1.register("Review",views.ViewSetReview,basename="ello4")
nested1.register('ProductImage',views.ViewSetProductImage)
nested2=routers.NestedDefaultRouter(parent_prefix='Carts',parent_router=router,lookup="cart")
nested2.register("Items",views.ViewSetCartItem,basename='ello5')
urlpatterns=router.urls+nested1.urls+nested2.urls