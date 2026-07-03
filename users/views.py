from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order

class RegisterView(View):

    def get(self, request):
        # показываем форму регистрации
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):

        form = UserCreationForm(request.POST)
        if form.is_valid():
            #save user and authorize him
            user = form.save()
            login(request, user)
            return redirect("products:product_list")
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form":form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("products:product_list")
        return render(request, 'users/login.html', {"form":form})

class LogoutView(View):

    def post(self, request):
        #exit with post, for CSRF secure
        logout(request)
        return redirect("products:product_list")

class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        #user orders history
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "users/profile.html", {"orders": orders})

class ProfileEditView(LoginRequiredMixin, View):

    def get(self, request):
        #redacting form with active orders
        form = UserChangeForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {"form": form})

    def post(self, request):
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'users/profile_edit.html', {"form": form})
