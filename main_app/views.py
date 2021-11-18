from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Cat
from main_app import models


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


# def cats_index(request):
#     cats = Cat.objects.all()
#     return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, pk):
    cat = Cat.objects.get(id=pk)
    return render(request, 'cats/detail.html', {'cat': cat})


class CatIndex(ListView):
    model = Cat
    template_name = 'cats/index.html'


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # success_url = '/cats/'


class CatUpdate(UpdateView):
    model = Cat
    fields = ('breed', 'description', 'age')


class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'