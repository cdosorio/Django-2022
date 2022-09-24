from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from projects.models import Project, Tag

def paginateProjects(request, projects, items_per_page):
    page = request.GET.get('page')
    paginator = Paginator(projects, items_per_page)
    
    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects_page = paginator.page(page)    
    except EmptyPage:
        page = paginator.num_pages
        projects_page = paginator.page(page) 
        
    left_index = (int(page)-4)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)
    if right_index >  paginator.num_pages:
        right_index = paginator.num_pages + 1               
        
    custom_range = range(left_index,right_index)
    return custom_range, projects_page


def searchProjects(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query') 
        
    # search in many to many relation
    tags = Tag.objects.filter(name__icontains=search_query)
        
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) | 
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return projects, search_query
    