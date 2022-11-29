from django.dispatch import receiver
from store.signals import order_created
@receiver(signal=order_created)
def order_created(sender,**kwargs):
    print(kwargs['order'])