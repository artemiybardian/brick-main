from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "date_of_birth", "country", "city")

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Проверяем размер файла (максимум 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5MB")
            # Проверяем расширение файла
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            import os
            ext = os.path.splitext(avatar.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Поддерживаются только изображения (jpg, jpeg, png, gif)")
        return avatar