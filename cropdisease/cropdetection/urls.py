from django.urls import path
from .views import CustomLoginView, custom_logout, upload_image_view

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('upload_image/', upload_image_view, name='upload_image'),
]