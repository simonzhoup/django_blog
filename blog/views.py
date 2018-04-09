from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'message':"Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request,'blog/index.html',context=context_dict)

def about(request):
    context_dict = {'message':'This tutorial has been put together by simon.'}
    return render(request,'blog/about.html',context=context_dict)
