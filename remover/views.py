from django.shortcuts import render
from django.http import JsonResponse
from .models import Photo
from backgroundremover.bg import remove
import os
from django.conf import settings


def remove_background_from_image(src_img_path, out_img_path):
    """Processes the image to remove its background."""
    model_choices = ["u2net", "u2net_human_seg", "u2netp"]
    with open(src_img_path, "rb") as f:
        data = f.read()
    img = remove(
        data,
        model_name=model_choices[0],
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_structure_size=10,
        alpha_matting_base_size=1000,
    )
    with open(out_img_path, "wb") as f:
        f.write(img)

def remove_bg(request):
    if request.method == 'POST' and request.FILES.get('original_picture'):
        # Save the original image to the database
        photo = Photo(original_picture=request.FILES['original_picture'])
        photo.save()

        # Define file paths for the input and output images
        src_img_path = photo.original_picture.path
        output_file_name = f"bg_removed_{photo.id}.png"
        out_img_path = os.path.join(settings.MEDIA_ROOT, "bg_removed_pic", output_file_name)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(out_img_path), exist_ok=True)

        # Process the image to remove background
        remove_background_from_image(src_img_path, out_img_path)

        # Update the Photo instance with the background-removed image
        photo.bg_removed_picture = f"bg_removed_pic/{output_file_name}"
        photo.save()

        # Prepare response with image URLs
        response_data = {
            'original_picture_url': photo.original_picture.url,
            'bg_removed_picture_url': photo.bg_removed_picture.url,
        }

        return JsonResponse(response_data)

    return render(request, 'index.html', {})