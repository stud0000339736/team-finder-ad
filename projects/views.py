from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProjectForm


def project_list(request):
    queryset = (
        Project.objects.all()
        .select_related('owner', 'skill')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'projects/project_list.html', context=context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    return render(request, 'projects/project-details.html', context=context)


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    form = ProjectForm(instance=project)

    if project.owner != user:
        return redirect('projects:project_list')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', pk=pk)

    context = {'form': form, 'id_edit': True}
    return render(request, 'projects/create-project.html', context=context)


@login_required
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    context = {}
    if project.status == 'open' and project.owner == user and request.method == 'POST':
        project.status = 'closed'
        project.save()
        context = {'status': 'ok', 'project_status': 'closed'}

    return JsonResponse(context)


@login_required
def project_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'})
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    if user in project.participants.all():
        project.participants.remove(user)
        participant = False
    else:
        project.participants.add(user)
        participant = True
    context = {'status': 'ok', 'participant': participant}
    return JsonResponse(context)


@login_required
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    if project in user.favorites.all():
        user.favorites.remove(project)
        favorited = False
    else:
        favorited = True
        user.favorites.add(project)
    context = {'status': 'ok', 'favorited': favorited}
    return JsonResponse(context)


@login_required
def get_favorites(request):
    user = request.user
    projects = (
        user.favorites.all()
        .select_related('skill', 'owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    context = {'projects': projects}
    return render(request, 'projects/favorite_projects.html', context=context)


@login_required
def create_project(request):
    is_edit = False
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            user = request.user
            project = form.save(commit=False)
            project.owner = user
            project.save()
            project.participants.add(user)
            return redirect('projects:project_detail', pk=project.pk)

    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'projects/create-project.html', context=context)
