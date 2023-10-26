"""
Còn nhiều function chx đc add vào. Khi nào team hội ý và thống nhất đc thì add vào sau.
"""

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.apps import AppConfig
import random
from django.db.models import Q
import datetime
import web3
import hashlib

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return redirect("a_login")
    return render(request, "registrations/login.html")


def Signup(request):
    edu = Education_rank.objects.all()
    context = {"educations":edu}
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        grade = request.POST.get("grade")
        education_rank = request.POST.get("edu_rank")
        description = request.POST.get("description")
        avatar = request.FILES['avatar']
        thumbnail = request.FILES['thumbnail']

        user = User.objects.filter(username=username).first()
        user2 = Bio.objects.filter(user=user).first()

        if not user and not user2:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = User.objects.get(username=username)
            if user:
                user2 = Bio(user=user, avatar=avatar, thumbnail=thumbnail, grade=grade,edu_rank=education_rank,
                               email=email, description=description)
                user2.save()
                login(request, user)
                return redirect("home")
        else:
            login(request, user)
            return redirect("home")
    return render(request, "registrations/register.html", context)

def index(request):
    return render("index.html")

def question_list_view(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Question.objects.filter(grade__lte=user.grade).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"question/list.html",context)

def gigs_list_view(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(grade__lte=user.grade, education_rank=user.edu_rank).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"gigs/list.html",context)

def document_list_view(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Document.objects.filter(grade__lte=user.grade, edu_rank=user.edu_rank).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"document/list.html",context)

def post_list_view(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"document/list.html",context)

def post_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            content = request.POST.get("content")
            sql = Post(content=content,like=0,dislike=0,user=user)
            sql.save()
            return redirect("post_view")
    else:
        return redirect("a_login")
    
def document_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            file = request.FILE.get("file")
            image = request.FILE.get("image")
            grade = request.POST.get("grade")
            edu_rank = request.POST.get("education_rank")

            sql = Document(title=title,description=description,file=file,image=image,grade=grade,edu_rank=edu_rank,like=0,dislike=0,user=user)
            sql.save()
            return redirect("document_view")
    else:
        return redirect("a_login")

def gigs_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            result = request.POST.get("result")
            image = request.FILE.get("image")
            grade = request.POST.get("grade")
            edu_rank = request.POST.get("education_rank")
            book = request.POST.get("book_include")
            type_learn = request.POST.get("type_learn")
            subject = request.POST.get("subject")
            price = request.POST.get("price")

            sql = Gigs(title=title,result=result,price=price,subject=subject,description=description,book=book,type_learn=type_learn,image=image,grade=grade,edu_rank=edu_rank,like=0,dislike=0,user=user)
            sql.save()
            return redirect("gigs_view")
    else:
        return redirect("a_login")
    
def question_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            file = request.POST.get("file")
            image = request.FILE.get("image")
            grade = request.POST.get("grade")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")
            price = request.POST.get("price")

            sql = Question(title=title,description=description,price=price,file=file,subject=subject,image=image,grade=grade,education_rank=edu_rank,like=0,dislike=0,user=user)
            sql.save()
            return redirect("gigs_view")
    else:
        return redirect("a_login")