from wagtail.users.forms import UserEditForm, UserCreationForm
from django import forms
from wagtail.images.widgets import AdminImageChooser
from wagtail.images import get_image_model


class CustomUserEditForm(UserEditForm):
    position = forms.DecimalField(decimal_places=0, max_digits=2)
    description = forms.Textarea()
    title = forms.CharField(max_length=50, required=False)
    tweeter = forms.URLField(max_length=100, required=False)
    github = forms.URLField(max_length=100, required=False)
    avatar = forms.ModelChoiceField(
        queryset=get_image_model().objects.all(), widget=AdminImageChooser(), label='Profile Picture', required=False,
    )
    bio = forms.Textarea()


class CustomUserCreationForm(UserCreationForm):
    position = forms.DecimalField(decimal_places=0, max_digits=2)
    description = forms.Textarea()
    title = forms.CharField(max_length=50, required=False)
    tweeter = forms.URLField(max_length=100, required=False)
    github = forms.URLField(max_length=100, required=False)
    avatar = forms.ModelChoiceField(
        queryset=get_image_model().objects.all(), widget=AdminImageChooser(), label='Profile Picture', required=False,
    )
    bio = forms.Textarea()