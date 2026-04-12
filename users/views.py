from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import UserRegisterForm, UserLoginForm, UserEditForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_2(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('projects:project_list')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_2(request):
    logout(request)
    return redirect('projects:project_list')


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'user': user}
    return render(request, 'users/user-details.html', context)


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', pk=request.user.pk)
    else:
        form = UserEditForm(instance=request.user)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile', pk=request.user.pk)
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/change_password.html', {'form': form})


def users_list(request):
    users = User.objects.all().order_by('-id')

    user = request.user

    filter_type = request.GET.get('filter')
    skill_id = request.GET.get('skill')

    active_skill = None

    if request.user.is_authenticated:
        if filter_type == 'owners-of-favorite-projects':
            users = users.filter(
                owned_projects__in=user.favorites.all()
            ).distinct()

        elif filter_type == 'owners-of-participating-projects':
            users = users.filter(
                owned_projects__participants=user
            ).distinct()

        elif filter_type == 'interested-in-my-projects':
            users = users.filter(
                favorites__owner=user
            ).distinct()

        elif filter_type == 'participants-of-my-projects':
            users = users.filter(
                participated_projects__owner=user
            ).distinct()

        if skill_id:
            users = users.filter(skill_id=skill_id)
            active_skill = skill_id

    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'participants': page_obj,
        'active_filter': filter_type,
        'active_skill': active_skill,
    }

    return render(request, 'users/participants.html', context)
