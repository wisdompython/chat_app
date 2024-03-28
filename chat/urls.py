from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("groups/<str:room_name>/<int:num>/", views.GroupChat, name="chat_room"),
    path("message/<int:user_id>/<int:num>/", views.private_chat_rooms, name='private_chat'),
    path('home',views.private_chat,name='home'),
    path('add_data',views.add_datasource,name='add_data'),
    path('add_collection',views.add_collection, name='add_collection'),
    path('query/<int:collection_id>', views.query_collection, name='query'),
    path('collections/col/',views.view_all_collections),
    path('group/create-group/', views.CreateGroupChat, name='groupchatmaker'),
    path('invite/acceptinvite/', views.AcceptGroupInvite, name='acceptinvite')
    
]