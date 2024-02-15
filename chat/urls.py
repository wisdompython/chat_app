from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("<str:room_name>/", views.room_view, name="chat_room"),
    path("message/<int:user_id>/", views.private_chat_rooms),
    path('home',views.private_chat,name='home')
]
