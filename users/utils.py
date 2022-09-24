from django.db.models import Q
from users.models import Profile, Skill


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