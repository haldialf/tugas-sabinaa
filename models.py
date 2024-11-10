from django.db import models
from django.contrib.auth.models import User
import os

#---------------------------------------------FILE UPLOAD----------------------------------------------#
class UploadedFile(models.Model):
    file_id = models.AutoField(primary_key=True)  # This will be the primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # Link to the user who uploaded the file
    file_type = models.CharField(max_length=20)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    file_location = models.FileField(upload_to='uploads/')  # Change to FileField for better file management
    upload_date_time = models.DateTimeField(auto_now_add=True)
    labels = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file_name  # Return the file name instead of default object string

    def is_image(self):
        # Check if file extension is for an image type
        return self.file_location.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.jfif'))

    def is_text_file(self):
        # Check if file extension is for a text file type
        return self.file_location.name.lower().endswith(('.txt', '.csv', '.md', '.log'))
    
    def is_audio_file(self):
    # Check if file extension is for an audio type
        return self.file_location.name.lower().endswith('.mp3')

    def is_video_file(self):
        # Check if file extension is for a video type
        return self.file_location.name.lower().endswith('.mp4')
    
    class Meta:
        db_table = 'file_uploaded'

class Profile(models.Model):
    USER_ROLES = [
        ('viewer', 'Viewer'),
        ('uploader', 'Uploader'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='viewer')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'  # This sets the custom table name to 'users'

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Create the profile if it doesn't exist
        Profile.objects.create(user=instance)


#------------------------------------------------ALBUM------------------------------------------------#
class Album(models.Model):
    album_name = models.CharField(max_length=255)
    display_pattern = models.CharField(max_length=20, choices=[  # Use CharField instead
        ('carousel', 'Carousel'),
        ('grid', 'Grid View'),
        ('slideshow', 'Slideshow'),
    ])
    created_date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.album_name


class AlbumMediaFiles(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album.album_name} - {self.file.file_name}"