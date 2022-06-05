from django.views.generic import TemplateView,CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')# クラスベースビューでURL解決する時に使う(renderの代わり？)

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'

class HomeView(TemplateView):
    template_name = 'accounts/home.html'
