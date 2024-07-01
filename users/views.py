from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import UserRegistrationForm, LoginForm, ProfileForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Account created successfully! You can now log in."
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error with your registration. Please try again."
        )
        return self.render_to_response(self.get_context_data(form=form))


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(
                self.request, "Invalid username or password. Please try again."
            )
            return self.form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "Logged out successfully!")
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile/profile.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile/edit_profile.html"
    success_url = reverse_lazy("view_profile")

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
