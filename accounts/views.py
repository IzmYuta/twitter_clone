from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import Http404

from .forms import LoginForm, SignUpForm, ProfileEditForm

User = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
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
    login_url = '/login/'


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response


class LogoutView(LogoutView):
    template_name = 'accounts/login.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = get_object_or_404(User, id=self.kwargs.get('pk', ''))
        return ctx


class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = User
    form_class = ProfileEditForm
    success_url = reverse_lazy('accounts:user_profile')

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk': self.object.pk})

    def get_form(self):
        form = super(UserProfileEditView, self).get_form()
        form.fields['username'].label = 'username'
        form.fields['email'].label = 'email'
        return form

    def test_func(self):
        if User.objects.filter(pk=self.kwargs['pk']).exists():
            current_user = self.request.user
            return current_user.pk == self.kwargs['pk']
        else:
            raise Http404
