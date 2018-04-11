from datetime import datetime

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .models import Category, Page


class IndexViews(generic.ListView):
    template_name = 'blog/index.html'


def get_server_side_cookie(request,cookie,defuale_value=None):
    val = request.session.get(cookie)
    if not val:
        val = defuale_value
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
    request.session['visits'] = visits


def index(request):
    request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:3]
    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response =  render(request, 'blog/index.html', context=context_dict)
    return response


def about(request):
    if request.session.test_cookie_worked():
        print('TEST COOKIE WORKED!')
        request.session.delete_test_cookie()
    context_dict = {'message': 'This tutorial has been put together by simon.'}
    return render(request, 'blog/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'blog/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'blog/add_category.html', {'form': form})

@login_required
def add_page(request, category):
    category = get_object_or_404(Category, slug=category)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=True)
            page.category = category
            page.save()
            return show_category(request, category.slug)
    else:
        print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'blog/add_page.html', context_dict)