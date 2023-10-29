"""
Còn nhiều function chx đc add vào. Khi nào team hội ý và thống nhất đc thì add vào sau.
"""

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .hashed import hashed
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
from web3 import Web3
from web3.middleware import geth_poa
import json
import hashlib
import os

web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/8c4c9235b7ed489ab0bc8c26795ae24e'))
web3.middleware_onion.inject(geth_poa, layer=0)
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')
contract = web3.eth.contract(address='0x70e787DA1E6dDA9AA8F4b91E9B029D360e04C7F3',abi=abi)

#authenticated
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

#index
def index(request):
    return render("index.html")

#list_view
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


#create_api
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

            if price >= 1:
                sql = Question(title=title,description=description,price=price,file=file,subject=subject,image=image,grade=grade,education_rank=edu_rank,like=0,dislike=0,user=user)
                sql.save()
                return redirect("gigs_view")
            else:
                sql = Question(title=title,description=description,price=1,file=file,subject=subject,image=image,grade=grade,education_rank=edu_rank,like=0,dislike=0,user=user)
                sql.save()
                return redirect("gigs_view")
    else:
        return redirect("a_login")
    
#payment_api
def question_payment(request,id):
    if request.user.is_authenticated:
        question = Question.objects.filter(id=id).first()
        if request.method == "POST" and question:
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                if final == bio.wallet_passcode and teen_balanced >= question.price:

                    os.environ["real_password"+bio] = bio.address_password
                    real_password = os.getenv("real_password"+bio)

                    tran = contract.functions.transfer(question.user.address, web3.toWei(question.price, 'ether')).buildTransaction(
                    {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                    signed_txn = web3.eth.account.signTransaction(tran, real_password)
                    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    return redirect("bill")
                else:
                    return redirect("retry_question_payment",time=1)
            else:
                return redirect("retry_question_payment",time=1)
            
def document_payment(request,id):
    if request.user.is_authenticated:
        document = Document.objects.filter(id=id).first()
        if request.method == "POST" and document:
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                if final == bio.wallet_passcode and teen_balanced >= document.price:

                    os.environ["real_password"+bio] = bio.address_password
                    real_password = os.getenv("real_password"+bio)

                    tran = contract.functions.transfer(document.user.address, web3.toWei(document.price, 'ether')).buildTransaction(
                    {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                    signed_txn = web3.eth.account.signTransaction(tran, real_password)
                    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    return redirect("bill")
                else:
                    return redirect("retry_question_payment",time=1)
            else:
                return redirect("retry_question_payment",time=1)
            
def gigs_payment(request,id):
    if request.user.is_authenticated:
        gigs = Gigs.objects.filter(id=id).first()
        if request.method == "POST" and gigs:
            code = request.POST.get("code")
            cls_day = request.POST.get("class_day")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                check = join_cls.objects.get(user=bio,gig=gigs)
                if final == bio.wallet_passcode and teen_balanced >= gigs.price and check:
                    learn = Learn.objects.filter(gig=gigs, check_stu=check).last()
                    if learn:
                        if cls_day > learn.cls_day:

                            sql = Learn(check_stu=check,cls_day=cls_day)
                            sql.save()

                            os.environ["real_password"+bio] = bio.address_password
                            real_password = os.getenv("real_password"+bio)

                            tran = contract.functions.transfer(gigs.user.address, web3.toWei(gigs.price, 'ether')).buildTransaction(
                            {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                            signed_txn = web3.eth.account.signTransaction(tran, real_password)
                            web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                            return redirect("bill")
                        else:
                            return redirect("retry_gig_payment",time=1)
                    else:
                            sql = Learn(check_stu=check,cls_day=1)
                            sql.save()

                            os.environ["real_password"+bio] = bio.address_password
                            real_password = os.getenv("real_password"+bio)

                            tran = contract.functions.transfer(gigs.user.address, web3.toWei(gigs.price, 'ether')).buildTransaction(
                            {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                            signed_txn = web3.eth.account.signTransaction(tran, real_password)
                            web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                            return redirect("bill")
                else:
                    return redirect("retry_gig_payment",time=1)
            else:
                return redirect("retry_gig_payment",time=1)
            
#read_api
"""
    Lưu Ý: 
        1. <name> = tên của tính năng (gigs: profile gia sư, post: bài đăng, ...)
        2. Có gì chưa rõ inbox hỏi lại em để đảm bảo khả năng hoạt động và tiến độ của dự án
        3. Lấy file gốc ở branch main trên github
        4. Khi up lại file thì up ở branch riêng (có name theo tên người) để tránh trường hợp nhiều bản đc đẩy lên cùng lúc
        5. Chưa chạy thử dự án để phòng trường hợp lỗi
        6. Edit trực tiếp tại https://github.dev/Codedr-edu/stempetition/tree/Anh-Minh/
    Cách Làm:
        B1. Tạo def read_<name>(request, id)
        B2. Tìm dòng có id = id đã khai báo trên ở CSDL và gán vào biến (nên đặt tên dễ hiểu)
        B3. Tạo dictionary giống như các api trên list_view
        B4. Render ra front-end (giống phần list_view)
    Tham Khảo:
        1. Các API trong phần list_view của dự án (Tổng Thể)
        2. https://docs.djangoproject.com/en/4.2/topics/db/queries/ (B2)
        3. https://www.w3schools.com/python/python_dictionaries.asp (B3)
        4. https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#render (B4)
        5. https://www.w3schools.com/django/index.php (Tổng Hợp)
        6. https://github.com/Codedr-edu/alclub (Dự án khác chỉ mang tính chất tham khảo thêm)
"""

#delete_api
"""
    Lưu Ý: 
        1. <name> = tên của tính năng (gigs: profile gia sư, post: bài đăng, ...)
        2. Có gì chưa rõ inbox hỏi lại em để đảm bảo khả năng hoạt động và tiến độ của dự án
        3. Lấy file gốc ở branch main trên github
        4. Khi up lại file thì up ở branch riêng (có name theo tên người) để tránh trường hợp nhiều bản đc đẩy lên cùng lúc
        5. Đối với xóa gigs, Post, Question, Document thì ko cần viết lệnh xóa phần comment & answer (em đã gán on_delete ở phần model.py nên nó sẽ tự xóa nếu nhx cái kia bị xóa)
        6. Đối với xóa comment và answer thì làm như bình thường
        7. Chưa chạy thử dự án để phòng trường hợp lỗi
        8. Edit trực tiếp tại https://github.dev/Codedr-edu/stempetition/tree/Anh-Huy/
    Cách Làm:
        B1. Tạo def delete_<name>(request, id)
        B2. Tìm dòng có id = id đã khai báo trên ở CSDL và thêm delete
        B3. redirect về trang list_view của tính năng đó (tên ở mục list_view)
    Tham Khảo:
        1. Các API khác của dự án (Tổng Thể)
        2. https://docs.djangoproject.com/en/4.2/topics/db/queries/ (B2.1)
        3. https://www.w3schools.com/django/django_delete_data.php (B2.2)
        4. https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect (B3)
        5. https://www.w3schools.com/django/index.php (Tổng Hợp)
        6. https://github.com/Codedr-edu/alclub (Dự án khác chỉ mang tính chất tham khảo thêm)
"""