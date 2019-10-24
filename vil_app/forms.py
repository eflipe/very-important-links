from django import forms
from django.contrib.auth.models import User
from vil_app.models import UserProfile


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', )
