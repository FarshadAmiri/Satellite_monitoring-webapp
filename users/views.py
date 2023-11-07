from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse ,reverse_lazy
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
from .models import *
from .forms import *


def login_view(request, *kwargs):
    if request.method =='GET':
        return render(request, 'Login_page.html')
    elif request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('fetch_data:SentinelFetch'))
        message = 'Invalid Credentials!'
        return render(request, 'Login_page.html', {'message':message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('fetch_data:SentinelFetch'))


# def signup_view(request):
#     if request.method == 'GET':
#         form = SignUpForm()
#         return render(request, 'Signup_page.html', {'form':form})
#     elif request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             Group.objects.get(name='Registered_users').user_set.add(user)
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return HttpResponseRedirect(reverse('flights:homepage'))
#         else:
#             return render(request, 'Error_page.html', {'message':form.errors})


def profile_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # user_profile = get_object_or_404(Profile, username=request.user.username)
            return render (request, 'Profile_page.html', {'user': request.user
                                                              # ,'user_profile': user_profile
                                                              })
        return HttpResponse('You Must Log In First')




# class update_profile_view(UpdateView):
#     model = User
#     fields = ['username', 'email', 'first_name', 'last_name', 'country', 'phone']
#     template_name = 'Update_Profile_Page.html'
#     success_url = reverse_lazy('flights:homepage')

#     def get_object(self, *args, **kwargs):
#         obj = super(update_profile_view, self).get_object(*args, **kwargs)
#         if obj == self.request.user:
#             return obj
#         raise Http404


# class change_password_view(View):
#     def get(self,request):
#         form = ChangePasswordForm()
#         return render(request, 'Change_Password_Page.html', context={'form':form})
#     def post(self,request):
#         form = ChangePasswordForm(request.POST)
#         if request.user.check_password(form.data['old_password']):
#             if form.data['new_password'] == form.data['new_password_repeated']:
#                 request.user.set_password(form.data['new_password'])
#                 request.user.save()
#                 return HttpResponseRedirect(reverse_lazy('users:profile'))
#             msg = 'Two passwords which you entered are not identical'
#         else:
#             msg = 'Your entered password was not correct'
#         return HttpResponseRedirect(reverse_lazy('flights:Error_page.html', msg))


# def delete_account_view(request):
#     # def get(self, request):
#     if request.method =='GET':
#         form = DeleteUserForm()
#         return render(request, 'Delete_User_Page.html', context={'user':request.user,
#                                                                  'form':form})
#     # def post(self, request):
#     elif request.method == 'POST':
#         form = DeleteUserForm(request.POST)
#         entered_password = form.data['password']
#         if request.user.check_password(entered_password):
#             username = request.user.username
#             user = User.objects.get(username=username)
#             user.is_active = False
#             logout(request)
#             user.delete()
#             return HttpResponse('You have been successfully deleted your user account')
#         super(delete_account_view)
#         return render(request, 'Delete_User_Page.html', context={'user':request.user,
#                                                                  'msg':'Wrong Password!'})
