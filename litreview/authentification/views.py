from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserFollows


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            context['error'] = True
            context['message'] = "Veuillez entrer vos identifiants"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reviews:index')
            else:
                context['error'] = True
                context['message'] = 'Utilisateur introuvable'

    return render(request, 'auth/login.html', context)


def is_username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


def signup(request):
    context = {}

    if request.POST:

        if request.POST['password'] != request.POST['password-confirm']:
            context['error'] = 'passwords'
            return render(request, 'auth/signup.html', context)

        if is_username_exists(request.POST['username']):
            context['error'] = 'username'
            return render(request, 'auth/signup.html', context)

        User.objects.create_user(
            request.POST['username'],
            password=request.POST['password']
        )

    return render(request, 'auth/signup.html', context)


@login_required
def auth_logout(request):
    logout(request)
    return redirect('authentification:index')


@login_required
def follows(request):
    context = {}
    if request.POST:
        username = request.POST['username']
        user = User.objects.get(username__exact=username)
        if user is not None:
            UserFollows.objects.create(user=request.user, followed_user=user)

    context['following'] = UserFollows.objects.filter(user__exact=request.user)
    context['followed_by'] = UserFollows.objects.filter(
        followed_user__exact=request.user
    )

    return render(request, 'auth/follows.html', context)


@login_required
def delete_follow(request, user_id):
    user = User.objects.get(id__exact=user_id)
    follow = UserFollows.objects.get(
        user__exact=request.user,
        followed_user__exact=user
    )
    if follow is not None:
        follow.delete()
    return redirect('authentification:follows')
