from django.shortcuts import redirect


def main_page(request):
    return redirect('projects:project_list')
