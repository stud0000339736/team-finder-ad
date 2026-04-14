from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.constants import STATUS_CLOSED, STATUS_OPEN
from core.service import paginate_queryset
from projects.forms import ProjectForm
from projects.models import Project


def project_list(request):
    queryset = (
        Project.objects.all()
        .select_related('owner', 'skill')
        .prefetch_related('participants')
    )

    page_obj = paginate_queryset(request, queryset)

    context = {'page_obj': page_obj}
    return render(request, 'projects/project_list.html', context=context)


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, 'projects/project-details.html', context=context)


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    form = ProjectForm(request.POST or None, instance=project)

    if project.owner != user:
        return redirect('projects:project_list')

    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', project_id=project_id)

    context = {'form': form, 'id_edit': True}
    return render(request, 'projects/create-project.html', context=context)


@login_required
def project_complete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    context = {}
    if project.status == STATUS_OPEN and project.owner == user and request.method == 'POST':
        project.status = STATUS_CLOSED
        project.save()
        context = {'status': 'ok', 'project_status': STATUS_CLOSED}

    return JsonResponse(context)


@login_required
def project_toggle(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'})

    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    is_participant = project.participants.filter(pk=user.pk).exists()

    if is_participant:
        project.participants.remove(user)
    else:
        project.participants.add(user)

    context = {'status': 'ok', 'participant': not is_participant}
    return JsonResponse(context)


@login_required
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    favorited = user.favorites.filter(pk=project.pk).exists()
    if favorited:
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    context = {'status': 'ok', 'favorited': not favorited}
    return JsonResponse(context)


@login_required
def get_favorites(request):
    user = request.user
    projects = (
        user.favorites.all()
        .select_related('skill', 'owner')
        .prefetch_related('participants')
    )
    context = {'projects': projects}
    return render(request, 'projects/favorite_projects.html', context=context)


@login_required
def create_project(request):
    is_edit = False
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        user = request.user
        project = form.save(commit=False)
        project.owner = user
        project.save()
        project.participants.add(user)
        return redirect('projects:project_detail', project_id=project.pk)

    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'projects/create-project.html', context=context)
