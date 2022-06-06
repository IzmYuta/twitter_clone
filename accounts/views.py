from django.views.generic import TemplateView,CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:home')# クラスベースビューでURL解決する時に使う(renderの代わり？)
    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url())#リダイレクト

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'

class HomeView(TemplateView):
    template_name = 'accounts/home.html'
