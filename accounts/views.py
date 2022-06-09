from django.views.generic import TemplateView,CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login


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
