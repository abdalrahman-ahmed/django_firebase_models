from django.urls import path

from fireapp.views import ApiView, LoginView, RegisterView, ChatView

urlpatterns = [
    path('', ApiView.as_view(), name='api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/', ChatView.as_view(), name='chat'),
]
