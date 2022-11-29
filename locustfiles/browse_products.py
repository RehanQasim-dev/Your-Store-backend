from http import client
from locust import HttpUser,task,between
from random import randint
class ProductUser(HttpUser):
    wait_time=between(2,5)
    @task
    def Product_list_in_collection(self):
        collect_id=randint(2,6)
        self.client.get(f'/store/Products/?collection_id={collect_id}',name='/store/Products')
    @task
    def Product_detail(self):
        product_id=randint(1,100)
        self.client.get(url=f'/store/Products/{product_id}/',name='/store/Products/:item')
    @task
    def create_cart(self):
        self.client.post(url='/store/Carts/',data={},name='/store/carts/:create')