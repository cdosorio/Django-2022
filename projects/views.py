from ast import For, Try
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.utils import paginateProjects, searchProjects
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm

# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects_page = paginateProjects(request, projects, 5)

    context = {'projects_page': projects_page, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        # due to property decorator, a parenthesis is not required
        project.getVoteCount
        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=project.id)

    return render(request, 'projects/single-project.html', {'project': project, 'form':form})


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    # Only the owner can update it
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')


    context = {'form': form, 'project':project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
     # Only the owner can delete it
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)

