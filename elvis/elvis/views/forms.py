import os, zipfile
from datetime import datetime
from random import choice

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from elvis.forms.entity import ComposerForm, CorpusForm, AttachmentForm, TagForm
from elvis.forms.user import UserForm, InviteUserForm
from elvis.forms.project import ProjectForm, DiscussionForm, CommentForm, TodoForm

from django.contrib.auth.models import User
from elvis.models.composer import Composer
from elvis.models.corpus import Corpus
from elvis.models.attachment import Attachment

'''
Views that create and add an entity to the database 
'''

def create_composer(request):
	picture = choice(os.listdir(os.path.abspath('elvis/media/generics/composers')))
	if request.method == 'POST':
		form = ComposerForm(request.POST)
		if form.is_valid():
			clean_form = form.cleaned_data
			# use **qwargs for additional data? 
			composer = Composer(name=clean_form['name'], 
								birth_date=clean_form['birth_date'], 
								death_date=clean_form['death_date'])
			composer.save()
			return HttpResponseRedirect('/uploads/success/')
	else:
		form = ComposerForm( initial={'name': 'Composer name', 
        							'birth_date': 'birth date', 
        							'death_date': 'death date'} )
	return render(request, 'forms/composer.html', {'form': form, 'picture':picture})


def create_corpus(request):
	picture = choice(os.listdir(os.path.abspath('elvis/media/generics/corpora')))
	if request.method == 'POST':
		form = CorpusForm(request.POST)
		if form.is_valid():
			clean_form = form.cleaned_data
			# use **qwargs for additional data? 
			corpus = Corpus(title=clean_form['title'], 
							comment=clean_form['comment'], 
							picture=clean_form['picture'],
							creator_id=400 )
			corpus.save()
			return HttpResponseRedirect('/uploads/success/')
	else:
		form = CorpusForm( initial={'title': 'Corpus name', 
        							'comment': 'This corpus is about...' } )
	return render(request, 'forms/corpus.html', {'form': form, 'picture':picture})


'''
Views that upload files to file system
'''
def upload_file(request):
	if request.method == 'POST':
		form = AttachmentForm(request.POST, request.FILES)
		if form.is_valid():
			file_handler(request.POST, request.FILES)
			return HttpResponseRedirect('/uploads/success')
	else:
		form = AttachmentForm()
	return render(request, 'forms/upload.html', {'form': form})

# Utility method that iterates over zip file
def fileiterator(zipf):
	with zipfile.ZipFile(zipf, "r", zipfile.ZIP_STORED) as openzip:
		filelist = openzip.infolist()
		for f in filelist:
			yield(f.filename, openzip.read(f))

# Saves an attachment and uploads file
def file_handler_helper(post, uploadedfile):
	f = Attachment()
	# Save first to generate pk for random file system
	f.save()
	f.uploader = User.objects.get(pk=40) 	# Hardcoded for now
	f.attachment = uploadedfile
	if post.get('description'):
		f.description = post['description']
	f.save()

# Handles upload of a file, whether single or zip
def file_handler(post, files):
	# If we have zip file upload multiple files with same description
	if files['attachment'].name.endswith('.zip'):
		for filename,content in fileiterator(files['attachment']):
			print filename
			file_handler_helper(post, filename)
	else:
		file_handler_helper(post, files['attachment'])
		

'''
View that deletes a model
'''

def delete_model(request):
	if request.method == 'POST':
		









