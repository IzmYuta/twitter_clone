from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            "gender",
            "self_intro",
        )
