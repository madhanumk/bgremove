from django.db import models

# Create your models here.


class Photo(models.Model):
    original_picture = models.ImageField(upload_to="original_pic")
    bg_removed_picture = models.ImageField(upload_to="bg_removed_pic",null=True,blank=True)