from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from .forms import FeedingForm

import boto3
import uuid

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-photo-uploads-daniel'


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

    toys_cat_doesnt_have = Toy.objects.exclude(
        id__in=cat.toys.all().values_list('id'))

    #  exclude objects in toys query that have pk's in this list [1, 4, 5]

    return render(
        request,
        'cats/detail.html', {
            'cat': cat,
            'feeding_form': feeding_form,
            'toys': toys_cat_doesnt_have
        })


def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    print(form._errors)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = pk
        new_feeding.save()

    return redirect('detail', pk=pk)


def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', pk=cat_id)


def add_photo(request, pk):
    photo_file = request.FILES.get('photo-file')

    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f'{S3_BASE_URL}{BUCKET}/{key}'
        photo = Photo(url=url, cat_id=pk)
        photo.save()
    except Exception as error:
        print(f'an error occurred uploading to AWS S3')
        print(error)
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