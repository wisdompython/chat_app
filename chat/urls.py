from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("<str:room_name>/", views.room_view, name="chat_room" )
]
