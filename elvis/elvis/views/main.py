from django.shortcuts import render


def home(request):
    return render(request, "home.html", {})


def search(request):
    return render(request, "search.html", {})


def corpus(request):
	return render(request, "corpus_list.html", {})

def composer(request):
	return render(request, "composer_list.html", {})

def piece(request):
	return render(request, "piece_list.html", {})

def movement(request):
	return render(request, "movement_list.html", {})
