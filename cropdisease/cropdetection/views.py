from django.shortcuts import render, redirect
from .models import UploadedImage, Result
from .utils import preprocess_image
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject

class CustomLoginView(LoginView):
    template_name = 'cropdetection/login.html'
    redirect_authenticated_user = True

@login_required(login_url='login')
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_image_view(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            processed_image, disease_type, confidence = preprocess_image(uploaded_image)

            # Use request.user directly without any changes
            user = request.user if request.user.is_authenticated else None
            uploaded_image_obj = UploadedImage.objects.create(user=user, image=processed_image)
            
            # Convert confidence to percentage
            confidence_percentage = round(confidence * 100.0, 2)
            
            result_obj = Result.objects.create(
                uploaded_image=uploaded_image_obj,
                disease_type=disease_type,
                confidence=confidence_percentage
            )

            # Pass disease and accuracy to the template
            context = {
                'disease_type': disease_type,
                'confidence': confidence_percentage,
                'processed_image': uploaded_image_obj.image.url,
            }

            # Redirect or render a response with the context
            return render(request, 'cropdetection/upload_success.html', context)

    # Render the form for uploading images
    return render(request, 'cropdetection/upload_image.html')