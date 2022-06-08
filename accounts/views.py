from django.views.generic import TemplateView,CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    #クラスベースビューでURL解決する時に使う(renderの代わり？)
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        #formの情報を保存
        user = form.save()
        #認証
        login(self.request, user)
        self.object = user
        #リダイレクト 
        return HttpResponseRedirect(self.get_success_url())

class WelcomeView(TemplateView):
    template_name = 'welcome/index.html'

class HomeView(TemplateView):
    template_name = 'accounts/home.html'
