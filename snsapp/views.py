from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreeCommentForm, FreePostForm
from .models import Post, FreePost

from urllib import response
import urllib.request
from dotenv import load_dotenv
import os
import folium


def home(request):
    # posts = Post.objects.all()
    posts = Post.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts': posts})


def postcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm()
    return render(request, 'detail.html', {'post_detail': post_detail, 'comment_form': comment_form})

# 댓글 저장


def new_comment(request, post_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Post, pk=post_id)
        finished_form.save()
    return redirect('detail', post_id)


def freehome(request):
    # posts = Post.objects.all()
    # freeposts = FreePost.objects.filter().order_by('-date')
    # return render(request, 'free_index.html', {'freeposts': freeposts})
    url = "https://openapi.map.naver.com/openapi/v3/maps.js?ncpClientId="
    url += client_id
    return render(request, 'map.html', {'mapUrl': url})


def freepostcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = FreePostForm(request.POST, request.FILES)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.author = request.user            # user 추가!
            unfinished.save()
            return redirect('freehome')
    else:
        form = FreePostForm()
    return render(request, 'free_post_form.html', {'form': form})


def freedetail(request, post_id):
    post_detail = get_object_or_404(FreePost, pk=post_id)
    comment_form = FreeCommentForm()
    return render(request, 'free_detail.html', {'post_detail': post_detail, 'comment_form': comment_form})


def new_freecomment(request, post_id):
    filled_form = FreeCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(FreePost, pk=post_id)
        finished_form.save()
    return redirect('freedetail', post_id)


load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_key = os.environ.get("CLIENT_KEY")


def load_map(request):

    # map_osm = folium.Map()
    # map_osm = folium.Map(location=[37.551718, 126.937803])

    # map_osm.save('map.html')
    url = "https://openapi.map.naver.com/openapi/v3/maps.js?ncpClientId="
    url += client_id
    return render(request, 'map.html', {'mapUrl': url})
    # return render(request, 'map.html')
