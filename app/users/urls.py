from django.urls import path, include

from .views import (
    UserIDView,
)

app_name = 'users'

urlpatterns = [
    path('user-id/', UserIDView.as_view(), name='user-id'),
]
