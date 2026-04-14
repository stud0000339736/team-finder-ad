from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from core.service import paginate_queryset
from users.forms import UserEditForm, UserLoginForm, UserRegisterForm
from users.models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')

    form = UserLoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('projects:project_list')


def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'users/user-details.html', context)


@login_required
def edit_user(request):
    form = UserEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('users:profile', user_id=request.user.pk)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('users:profile', user_id=request.user.pk)

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

    page_obj = paginate_queryset(request, users)

    context = {
        'participants': page_obj,
        'active_filter': filter_type,
        'active_skill': active_skill,
    }

    return render(request, 'users/participants.html', context)
