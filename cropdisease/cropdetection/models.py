from django.db import models
from django.contrib.auth.models import User


class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_images')
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"


class Result(models.Model):
    uploaded_image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='result')
    disease_type = models.CharField(max_length=255)
    confidence = models.FloatField()
    result_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.uploaded_image.user.username} - {self.disease_type}"