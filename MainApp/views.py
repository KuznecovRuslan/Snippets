from django.contrib import auth
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета'}
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snippets-list')


def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов'}

    snippets = Snippet.objects.all

    context = {
        "snippets": snippets,

    }

    return render(request, 'pages/view_snippets.html', context)


def snippets_create(request):

    if request.method == "POST":
        # print(request.POST)

        # name = request.POST["name"]
        # lang = request.POST["lang"]
        # code = request.POST["code"]
        # snippet = Snippet(name=name, lang=lang, code=code)
        # snippet.save()
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snippets-list')

    raise Http404


def snippet_edit(request, id):
    if request.method == "GET":
        snippet = get_object_or_404(Snippet, pk=id)
        form = SnippetForm(instance=snippet)

        context = {'pagename': 'Изменение сниппета ' + str(id)}
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
        snippet = get_object_or_404(Snippet, pk=id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippets-list')


def login_page(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           context = {}
           context["error"] = "Не верный логин или пароль"
           return render(request, 'index.html', context)
   return redirect('home')

def logout(request):
    auth.logout(request)
    return redirect('home')