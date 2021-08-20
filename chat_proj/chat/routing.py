from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    #\w+ will match one or more alpha,digi,and underscore and pass it as variable 'room_name'
    re_path(r'ws/chat/(?P<room_name>\w+)/$',consumers.ChatRoomConsumer),
    
    #for safety
    # re_path(r'^ws/chat/(?P<room_name>[^/]+)/$',consumers.ChatRoomConsumer),
]