from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import Profile, Skill

def paginateProfiles(request, profiles, items_per_page):
    page = request.GET.get('page')
    paginator = Paginator(profiles, items_per_page)
    
    try:
        profiles_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles_page = paginator.page(page)    
    except EmptyPage:
        page = paginator.num_pages
        profiles_page = paginator.page(page) 
        
    left_index = (int(page)-4)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)
    if right_index >  paginator.num_pages:
        right_index = paginator.num_pages + 1               
        
    custom_range = range(left_index,right_index)
    return custom_range, profiles_page


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query') 
        
    # Search in another model
    skills = Skill.objects.filter(name__icontains=search_query)
            
    # use Q to search by multiple fields
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )
    return profiles, search_query