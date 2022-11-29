from django.utils.html import format_html, urlencode
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from  . import models

# Register your models here.
admin.site.site_header="MYSTORE"
admin.site.index_title="Resources"

#-------------------------------------------------------------------------
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','user','phone','membership','birth_date']    #does not accept lookup fields
    ordering=['user__first_name']#accepts lookup fields does not accept method fields
    list_editable=['membership']    
    search_fields=["first_name"]  #it can be method fields also accepts lookups
    list_per_page=10
@admin.register(models.Collection)
#-----------------------------------------------------------------
class CollectionAdmin(admin.ModelAdmin):
    list_display=["title","No_of_products"]
    search_fields=["title__istartswith"]
    @admin.display(ordering="No_of_products")
    def No_of_products(self,mone:models.Product):
        print("Im in no of products")
        print(mone)
        url=reverse('admin:store_product_changelist')+"?"+urlencode({"collection__id":str(mone.id)})
        return format_html('<a href={}>{}</a>',url,mone.No_of_products)
    def get_queryset(self, request):
        print("im in get query")
        return super().get_queryset(request).annotate(No_of_products=Count("product"))
#-----------------------------------------------------------------------------
class InventoryFilter(admin.SimpleListFilter):
    title="Inventory"
    parameter_name="inventory"
    def lookups(self, request, model_admin):#2nd
        print("im in lookups_query")
        return [("<10","Less than 10")]
    def queryset(self, request,queryset):#third
        print("Im in filter_query")
        print(f"self= {type(self)}, {self}")
        print("queryset= ",queryset.query)
        if self.value() =="<10":
            return queryset.filter(inventory__lt=10)
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # autocomplete_fields=["collection"]
    prepopulated_fields={"slug":["title"]}
    radio_fields={"collection":admin.HORIZONTAL}
    exclude=["last_update"]
    raw_id_fields=['collection']
    list_display=['id','title',"Collection","inventory_status","price"]
    list_select_related=True
    list_editable=["price"]
    list_filter=["collection","last_update",InventoryFilter]
    search_fields=["title"]
    ordering=["id"]  
    # def get_ordering(self, request):
    #     return ['title']
    @admin.display(ordering="collection__title")
    def Collection(self,obj):
        # print("self type=",type(self))
        # print("object type = ",type(obj))
        print("/nIm in productadmin Collection method")   #both methods are alternatively
                                                            #called according to
                                                            # the order given in display list
                                                            # for each record once 
        return obj.collection.title
    def inventory_status(self,query:models.Product):
        print("/nIm in productadmin inventory_status method")
        if query.inventory<10:
            return "Low"
        else:
            return "High"
    def get_queryset(self, request):#first
        print("the super query is  ",super().get_queryset(request).query)
        return super().get_queryset(request)
#------------------------------------------------------------------------------
class OrderItem(admin.TabularInline):
    model=models.OrderItem
    def ello(self,prodc):
        return prodc.product.price
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    inlines=[OrderItem]
    list_display=["id","placed_at","customer"]
    autocomplete_fields=["customer"]


    
