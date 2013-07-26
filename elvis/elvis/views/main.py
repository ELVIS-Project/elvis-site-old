from django.shortcuts import render
from elvis.models.composer import Composer
from elvis.models.download import Download
from django.http import HttpResponse

from elvis.models.userprofile import UserProfile
from elvis.models.project import Project
from elvis.models.todo import Todo
from elvis.models.discussion import Discussion
from elvis.models.comment import Comment

HTTP_METHODS = ['GET', 'PUT', 'POST', 'HEAD', 'TRACE', 'DELETE', 'OPTIONS']


# Render the home page 
def home(request):
    return render(request, "home.html", {})

# Render the upload page 
def upload(request):
	return render(request, "upload.html", {})

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
    todos = Todo.objects.all()
    discussions = Discussion.objects.filter(project_id=pk)
    comments = {}
    users = {}
    for discussion in discussions:
        comments[discussion.id] = Comment.objects.filter(discussion_id=discussion.id).order_by('-created')
    context = {'content':project, 
                'todos': todos, 
                'discussions':discussions, 
                'comments':comments}
    return render(request, 'project/project_detail.html', context)


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