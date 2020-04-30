import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
from .forms import TweetForm

# Create your views here.
def home_view(request,*args,**kwargs):
    return render(request,'pages/home.html',context={},status=200)

def tweet_create_view(request,*args,**kwargs):
    form  = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    print('next url ',next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url!=None and is_safe_url(next_url,settings.ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html',context = {"form":form})

def tweet_list_view(request,*args, **kwargs):
    qs = Tweet.objects.all()    
    tweets_list = [{"id": x.id, "content":x.content,"likes":random.randint(0,15151)} for x in qs]
    data = {

        "response":tweets_list,
    }
    return JsonResponse(data,status=200)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    status = 200
    data = {
        "id":tweet_id,
    }
    try:

        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "NOT FOUND"
        status = 404
    
    return JsonResponse(data,status=status)
    