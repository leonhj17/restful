from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
# def user_login(request):
#     if request.method == 'GET':
#         login_form = LoginForm()
#         return render(request, 'login.html', {
#             'form': login_form,
#         })
#
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             cd = login_form.cleaned_data
#             user = authenticate(**cd)
#
#             if user:
#                 login(request, user)
#                 return render(request, 'page_home.html')
#             else:
#                 return HttpResponse('login failed')
#         return HttpResponse('invail input')
def validate_username(request):
    username = request.GET.get('username', '')
    date = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(date)


def validate_username2(request):
    username = request.GET.get('username', '')
    date = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if date['is_taken']:
        date['error_message'] = 'user do not exist.'
    return JsonResponse(date)
