from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email',)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
        ]

    def __init__(self, email=None, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email
        if username:
            self.fields['username'].widget.attrs['value'] = username


    def update(self, user):
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.save()
