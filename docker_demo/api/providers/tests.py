# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from providers.models import Provider


class ProviderViewTestCase(APITestCase):
    url_reverse = reverse('api:provider-list')
    url = '/api/provider/'
    url_detail = '/api/provider/{}/'
    url_detail_route_reverse = reverse('api:provider-detail', kwargs={"pk": 1})
    url_detail_route = '/api/provider/{}/detail/'
    url_list_route = '/api/provider/all_providerName/'

    def setUp(self):
        print('setUp')

        self.client = APIClient()
        # create user
        User.objects.create_user(username='test_user', password='password123')

        self.client.login(username='test_user', password='password123')

        self.request_data = {
            'providerID': 'providerID_test',
            'providerName': 'providerName_test'
        }

        self.provider = Provider.objects.create(providerID='providerID_test', providerName='providerName_test')

    def test_api_provider_create(self):
        print('test_api_provider_create')
        self.response = self.client.post(
            self.url,
            self.request_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 2)
        self.assertEqual(Provider.objects.get(pk=self.provider.id).providerID, 'providerID_test')
        self.assertEqual(Provider.objects.get(pk=self.provider.id).providerName, 'providerName_test')

    def test_api_provider_retrieve(self):
        print('test_api_provider_retrieve')
        provider = Provider.objects.get(pk=self.provider.id)
        response = self.client.get(self.url_detail.format(self.provider.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('providerID', None), provider.providerID)
        self.assertEqual(response.data.get('providerName', None), provider.providerName)

    def test_api_provider_partial_update(self):
        print('test_api_provider_partial_update')
        update_providerID = {'providerID': 'providerID_update'}
        response = self.client.patch(self.url_detail.format(self.provider.id), update_providerID, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('providerID', None), update_providerID.get('providerID', None))

    def test_api_provider_update(self):
        print('test_api_provider_update')
        update_providerID = {'providerID': 'providerID_update', 'providerName': 'providerName_update'}
        response = self.client.put(self.url_detail.format(self.provider.id), update_providerID, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('providerID', None), update_providerID.get('providerID'))
        self.assertEqual(response.data.get('providerName', None), update_providerID.get('providerName'))

    def test_api_provider_delete(self):
        print('test_api_provider_delete')
        response = self.client.delete(self.url_detail.format(self.provider.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_provider_detail_route(self):
        print('test_api_provider_detail_route')
        provider = Provider.objects.get(pk=self.provider.id)
        response = self.client.get(self.url_detail_route.format(self.provider.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('providerID', None), provider.providerID)
        self.assertEqual(response.data.get('providerName', None), provider.providerName)

    def test_api_provider_list_route(self):
        print('test_api_provider_list_route')
        provider = Provider.objects.values_list('providerName', flat=True).distinct()
        response = self.client.get(self.url_list_route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(next(iter(response.data)), next(iter(provider)))
