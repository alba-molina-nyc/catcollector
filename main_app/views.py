from django.db.models import fields
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Cat, Toy
from .forms import FeedingForm
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

    feeding_form = FeedingForm()

    return render(
        request,
        'cats/detail.html', {
            'cat': cat,
            'feeding_form': feeding_form
        })


def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    print(form._errors)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = pk
        new_feeding.save()

    return redirect('detail', pk=pk)


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


class ToyCreate(CreateView):
    model = Toy
    fields = ('name', 'color')


class ToyUpdate(UpdateView):
    model = Toy
    fields = ('name', 'color')


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'


class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'