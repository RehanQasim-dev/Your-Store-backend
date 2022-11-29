
from urllib import response

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest
@pytest.mark.django_db
class TestCreateCollections:
    def test_if_user_is_anonymous_return_401(self):
        client=APIClient()
        respon=client.post('/store/Collections/',{'title':'ello'})
        assert respon.status_code==status.HTTP_401_UNAUTHORIZED
    def test_if_user_is_auth_but_not_staff_return_403(self):
        client=APIClient()
        client.force_authenticate(user=[])
        respon=client.post('/store/Collections/',{'title':'ello'})
        assert respon.status_code==status.HTTP_403_FORBIDDEN
    def test_if_user_isstaff_and_valid_data_return_201(self):
        client=APIClient()
        client.force_authenticate(user=User(is_staff=True))
        respon=client.post('/store/Collections/',{'title':'ello'})
        print(response)
        assert respon.status_code==status.HTTP_201_CREATED
    def test_if_user_isstaff_and_invalid_data_return_400(self):
        client=APIClient()
        client.force_authenticate(user=User(is_staff=True))
        respon=client.post('/store/Collections/',{'title':''})
        assert respon.status_code==status.HTTP_400_BAD_REQUEST
    
    
