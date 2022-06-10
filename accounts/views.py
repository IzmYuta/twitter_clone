from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self,form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response 
        

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class LoginView(TemplateView):
    template_name = 'accounts/login.html'
