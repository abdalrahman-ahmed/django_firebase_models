from django.urls import path

from fireapp.views import APIRoot, LoginView, RegisterView, ChatView

urlpatterns = [
    path('', APIRoot.as_view(), name='api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/', ChatView.as_view(), name='chat'),
]
