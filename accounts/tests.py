from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import  APITestCase

class userProfileTestCase(APITestCase):
    profile_list_url = reverse('all-profiles')

    def setUp(self):
        #create new users
        self.user = self.client.post('/auth/users/', data = {'username': 'mario', 'password': 'i-keep-jumping' })
        #get json token
        response = self.client.post('/auth/jwt/create/', data = {'username': 'mario', 'password': 'i-keep-jumping'})
        self.token = response.data['access']
        self.api_authentication()


    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer' + self.token)


    #get profile authenticated
    def test_userprofile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #get user profile failed authenticated
    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticated(self)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #check authorisation profile
    def test_userprofile_detail_retrieve(self):
        response = self.client.get(reverse('profile', kwargs = {'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #authomatic add user data
    def test_userprofile_profile(self):
        profile_data = {'description': 'I am a bat man ', 'location': 'nintendo', 'is_creator': 'true',}
        response = self.client.put(reverse('profile', kwargs = {'pk': 1}, data = profile_data))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





