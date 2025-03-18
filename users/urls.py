from django.urls import path # type: ignore
from .views import user_form_view

urlpatterns = [
    path('', user_form_view, name='user_form'),
]
