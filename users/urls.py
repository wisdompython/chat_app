from django.urls import path
from .views import *

urlpatterns = [
    path('user_search', FindFriends, name='user_search'),
    path('user_profile/<int:user_id>', ViewUserProfile, name='user_profile'),
    path('test_search/<str:user_mail>/', testsearch, name='test_search')
]