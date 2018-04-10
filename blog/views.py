from django.shortcuts import render,get_object_or_404
from django.views import generic

from .forms import CategoryForm,PageForm, UserForm, UserProfileForm
from .models import Category,Page


class IndexViews(generic.ListView):
    template_name = 'blog/index.html'

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:3]
    context_dict = {
        'categories':category_list,
        'pages':page_list,
    }
    return render(request,'blog/index.html',context=context_dict)


def about(request):
    context_dict = {'message':'This tutorial has been put together by simon.'}
    return render(request,'blog/about.html',context=context_dict)

def show_category(request,category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request,'blog/category.html',context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'blog/add_category.html',{'form':form})

def add_page(request,category):
    category = get_object_or_404(Category,slug=category)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=True)
            page.category = category
            page.save()
            return show_category(request,category.slug)
    else:
        print(form.errors)
    context_dict = {'form':form,'category':category}
    return render(request,'blog/add_page.html',context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                print('ok')
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserProfileForm

    return render(request,
                  'blog/register.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})
