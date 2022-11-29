from django.http import HttpResponse
from .tasks import first_task
# import requ

# Create your views here.
# def task_manager(request):
#     '''If we use perform the task this way then our view function of 
#     or request handler will wait for the its returned value and then
#     proceed but if we are not using its returned value then why should
#     we halt till the value is returned so in such tasks asked by the client
#     we can give the response immediately and let the process happen in the background'''
#     'for background task use this'
#     first_task.delay("hello! Im here")
#     return HttpResponse('Response Returned')
# def task_manager(request)if ()
# if ()