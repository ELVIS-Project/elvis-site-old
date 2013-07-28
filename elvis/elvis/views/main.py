import sys, operator
import elvis.models

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from elvis.models.attachment import Attachment
from elvis.models.composer import Composer
from elvis.models.download import Download
from elvis.models.comment import Comment
from elvis.models.userprofile import UserProfile
from elvis.models.project import Project
from elvis.models.todo import Todo
from elvis.models.discussion import Discussion
from elvis.models.comment import Comment

def get_models(models):
    return filter(lambda mod: not mod.startswith('__') or mod[0].islower(), models)

HTTP_METHODS = ['GET', 'PUT', 'POST', 'HEAD', 'TRACE', 'DELETE', 'OPTIONS']
MODELS = get_models(dir(elvis.models))

# Render the home page 
def home(request):
    return render(request, "home.html", {})

# Render the upload page 
def upload(request):
	return render(request, "upload.html", {})

def relevant_field(field): 
    field = str(field)
    return 'CharField' in field or 'TextField' in field or 'DateField' in field

def filter_dates(results, start, end):
    # This means should only look at dates related to objects found
    if results:
        for result in results:
            # Iterate through each result set and get all related pk's w/ dates
            # Can reduce complexity by just hardcoding which ones have dates? 
    # Otherwise just return all objects in this range
    else:



def filter_voices(results, voices):
    # This means should only look at voices related to objects found
    if results:
        
    # Otherwise just return all objects with this number of voices
    else:

# Must search CharField, TextField, DateField of all models in specified filters
def search(query, exclude, filters):
    # Exclude should be comma-separated list
    exclude_queries = []
    if exclude:
        exclude_queries = exclude.split(',')
    # If no filter specified, just look through all the models
    if not filters:
        filters = MODELS
    results = []
    for category in filters:
        # Get class associated with filter
        model = getattr(elvis.models, category.title())
        # Get relevant attributes of this class
        fields = filter(lambda field: relevant_field(field), model._meta.fields)
        # Create query key, value pairs for included and excluded search params
        included = map(lambda field: (field.name+'__icontains', query), fields)
        excluded = []
        for eq in excluded_queries:
            for field in fields:
                excluded.append( (field.name+'__icontains', eq) )
        field_tuples = included + excluded
        if not field_tuples:
            break
        # Create conjunction of fields for query 
        qset = reduce(operator.or_, (Q(**{field: query}) for field, query in field_tuples))
        result = model.objects.filter(qset).exclude()
        if result:
            results.append(result)
    return results

# TODO: Need to return items related to search param
# TODO: Should they be able to query primary keys/ids? 
# Query database based on search terms
def search_view(request):
    if request.method == "GET":
        query = request.GET.get('search')
        exclude = request.GET.get('exclude')
        start_year = request.GET.get('start-year')
        end_year = request.GET.get('end-year')
        piece = request.GET.get('piece')
        movement = request.GET.get('movement')
        composer = request.GET.get('composer')
        user = request.GET.get('user')
        discussion = request.GET.get('discussion')
        log = request.GET.get('log')
        voices = request.GET.get('num-voices')

    # Create list of filters
    raw_filters = [piece, movement, composer, user, discussion, log]
    filters = filter(lambda x:x is not None and x.title() in MODELS, raw_filters)

    # If there is a basic query, search for it
    if query:
        results = search(query, exclude, filters)
        # Now filter further on dates
        results = filter_dates(results, start_year, end_year)
        # Now filter further on #of voices
        results = filter_voices(results, voices)

    # Otherwise check for other conditions 
    else:
        results = []
        # Return all objects from filter categories
        for category in filters:
            model = getattr(elvis.models, category.title())
            results.append(model.objects.all())
        # Now filter further on dates
        results = filter_dates(results, start_year, end_year)
        # Now filter further on #of voices
        results = filter_voices(results, voices)
    
    return render(request, 'search_results.html', {"results": results})

# Partition data into rows. Used for template organization
def partition(data, row):
    partitioned_data = []
    for x in range(0, len(data), row):
        partitioned_data.append(data[x:x+row])
    return partitioned_data

# Render list of user profiles
def user_profiles(request):
    userprofiles = UserProfile.objects.all()
    userprofiles_list = partition(userprofiles, 4)
    return render(request, 'userprofile/userprofile_list.html', {'content': userprofiles_list, 'length':len(userprofiles)})

def user_view(request, pk):
    user = UserProfile.objects.filter(pk=pk)[0]
    return render(request, 'userprofile/userprofile_detail.html', {'content':user})

def projects_list(request):
    projects = Project.objects.all()
    projects_list = partition(projects, 3)
    return render(request, 'project/project_list.html', {'projects': projects_list, 'length':len(projects)})

def project_view(request, pk):
    project = Project.objects.filter(pk=pk)[0]
    todos = Todo.objects.filter(project_id=pk)
    discussions = Discussion.objects.filter(project_id=pk)
    comments = {}
    for discussion in discussions:
        comments[discussion.id] = Comment.objects.filter(discussion_id=discussion.id).order_by('-created')
    context = {'content':project, 
                'todos': todos, 
                'discussions':discussions, 
                'comments':comments}
    return render(request, 'project/project_detail.html', context)

def project_participants(request, pk):
    project = Project.objects.filter(pk=pk)[0]
    return render(request, 'project/project_participants.html', {"content": project})

def project_discussions(request, pk):
    project = Project.objects.filter(pk=pk)[0]
    discussions = Discussion.objects.filter(project_id=pk)
    num_comments = {}
    for discussion in discussions:
        num_comments[discussion.id] = Comment.objects.filter(discussion_id=discussion.id).count()
    context = {"project": project, 
                "discussions": discussions,
                "comments": num_comments}
    return render(request, 'project/project_discussions.html', context)

def discussion_view(request, pk, did):
    if request.method == "POST":
        comment = request.POST.get('comment')
        obj = Comment(name='', text=comment, user_id=400, discussion_id=did)
        obj.save()
    project = Project.objects.get(pk=pk)
    discussion = Discussion.objects.get(pk=did)
    comments = Comment.objects.filter(discussion_id=did)
    context = {"project": project, "discussion": discussion, "comments": comments}
    return render(request, 'discussion/discussion_detail.html', context)
        

# Used across html files to save items to download later
# TODO: How to get current user? 
def save_downloads(request):
    if request.method == 'POST':
        items = request.getlist("items")
        # Need to save these items to the database
        for item in items:
        	obj = Download(item)
        	obj.save()
    # Now render downloads page 
    return render(request, "download.html", {})