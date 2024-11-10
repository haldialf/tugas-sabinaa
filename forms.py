from django import forms
from .models import UploadedFile, Album
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#---------------------------------------------FILE UPLOAD----------------------------------------------#
class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)  # Add the file field
    class Meta:
        model = UploadedFile
        fields = ['labels']  # Let the user fill out the file name and labels
    

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#------------------------------------------------ALBUM------------------------------------------------#
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_name', 'display_pattern']

class MediaFileSelectionForm(forms.Form):
    media_files = forms.ModelMultipleChoiceField(
        queryset=UploadedFile.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MediaFileSelectionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['media_files'].queryset = UploadedFile.objects.filter(user=user)