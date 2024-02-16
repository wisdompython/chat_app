from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("<str:room_name>/", views.room_view, name="chat_room"),
    path("message/<int:user_id>/", views.private_chat_rooms),
    path('home',views.private_chat,name='home'),
    path('add_data',views.add_datasource),
    path('add_collection',views.add_collection),
    path('query/<int:collection_id>', views.query_collection, name='query'),
    path('collections/col/',views.view_all_collections)
]
