"""
Còn nhiều function chx đc add vào. Khi nào team hội ý và thống nhất đc thì add vào sau.
"""

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .hashed import hashed, create_wallet
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
        passcode = request.POST.get("passcode")

        user = User.objects.filter(username=username).first()
        user2 = Bio.objects.filter(user=user).first()

        if not user and not user2:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = User.objects.get(username=username)
            if user:
                wallet = create_wallet()
                user2 = Bio(user=user, avatar=avatar, thumbnail=thumbnail, grade=grade,edu_rank=education_rank,
                               email=email, description=description, address=wallet, address_password=wallet.privateKey.hex(), wallet_passcode = wallet)
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

#searched_list_view
def searched_question_list_view(request,q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Question.objects.filter(Q(title__icontain=q) | Q(description__icontain=q),grade__lte=user.grade).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"question/list.html",context)

def searched_gigs_list_view(request,q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(Q(title__icontain=q) | Q(description__icontain=q),grade__lte=user.grade, education_rank=user.edu_rank).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"gigs/list.html",context)

def searched_document_list_view(request,q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Document.objects.filter(Q(title__icontain=q) | Q(description__icontain=q),grade__lte=user.grade, edu_rank=user.edu_rank).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"document/list.html",context)

def searched_post_list_view(request,q):
    if request.user.is_authenticated:
        post = Post.objects.filter(Q(content__icontain=q)).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"document/list.html",context)


def searched_trade_list_view(request,q):
    if request.user.is_authenticated:
        post = Trade.objects.filter(Q(title__icontain=q) | Q(description__icontain=q)).all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"trade/list_view.html",context)

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


def trade_list_view(request):
    if request.user.is_authenticated:
        post = Trade.objects.all()
        context = {"posts":post[::-1]}
    else:
        return redirect("a_login")
    return render(request,"trade/list_view.html",context)

#create_api
def post_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            content = request.POST.get("content")
            sql = Post(content=content,user=user)
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
            price = request.POST.get("price")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")

            sql = Document(title=title,description=description,file=file,image=image,grade=grade,edu_rank=edu_rank,user=user,price=price,subject=subject)
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

            sql = Gigs(title=title,result=result,price=price,subject=subject,description=description,book=book,type_learn=type_learn,image=image,grade=grade,edu_rank=edu_rank,user=user)
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
                sql = Question(title=title,description=description,price=price,file=file,subject=subject,image=image,grade=grade,education_rank=edu_rank,user=user)
                sql.save()
                return redirect("gigs_view")
            else:
                sql = Question(title=title,description=description,price=1,file=file,subject=subject,image=image,grade=grade,education_rank=edu_rank,user=user)
                sql.save()
                return redirect("gigs_view")
    else:
        return redirect("a_login")
    
def create_trade_offer(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if bio and request.method == "POST":
            change_value = request.POST.get("change_value")
            change_currency = request.POST.get("change_currency")
            changed_currency = request.POST.get("changed_currency")

            if change_currency and change_value and changed_currency:
                if changed_currency == "ETH":
                    changed_value = 0.00022 * change_value
                    sql = Trade(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn")
                    sql.save()
                    sql = Trade.objects.filter(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn",user=bio).first()
                    return redirect("read_trade_offer",id=id)
                elif changed_currency == "VND":
                    changed_value = 10000 * change_value
                    sql = Trade(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn")
                    sql.save()
                    sql = Trade.objects.filter(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn",user=bio).first()
                    return redirect("read_trade_offer",id=id)
                elif changed_currency == "USD":
                    changed_value = 0.41 * change_value
                    sql = Trade(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn")
                    sql.save()
                    sql = Trade.objects.filter(changed_value=change_value,changed_value=changed_value,change_currency=change_currency,changed_currency=changed_currency,payment_method=changed_currency,done="Còn hạn",user=bio).first()
                    return redirect("read_trade_offer",id=id)
            else:
                return redirect("create_trade_offer_view",id=id)
    
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

                    os.environ["real_password_question"+bio.user.username] = bio.address_password
                    real_password = os.getenv("real_password_document"+bio.user.username)

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

                    os.environ["real_password_document"+bio.user.username] = bio.address_password
                    real_password = os.getenv("real_password_document"+bio.user.username)

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

                            os.environ["real_password_gigs"+bio.user.username] = bio.address_password
                            real_password = os.getenv("real_password_gigs"+bio.user.username)

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

                            os.environ["real_password_gigs"+bio.user.username] = bio.address_password
                            real_password = os.getenv("real_password_gigs"+bio.user.username)

                            tran = contract.functions.transfer(gigs.user.address, web3.toWei(gigs.price, 'ether')).buildTransaction(
                            {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                            signed_txn = web3.eth.account.signTransaction(tran, real_password)
                            web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                            return redirect("bill")
                else:
                    return redirect("retry_gig_payment",time=1)
            else:
                return redirect("retry_gig_payment",time=1)
            
#trade_api
def eth_to_teen(request,id):
    if request.user.is_authenticated:
        post = Trade.objects.filter(id=id).first()
        if request.method == "POST" and post and post.change_currency.name == "ETH" and post.changed_currency.name == "Teen":
            code = request.POST.get("passcode")
            if code:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                    teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                    eth_balanced = float(eth_balanced = float(web3.toWei(web3.eth.getBalance(post.user.address),'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        os.environ["real_password_teen"+bio.user.username] = bio.address_password
                        real_password = os.getenv("real_password_teen"+bio.user.username)

                        tran = contract.functions.transfer(post.user.address, web3.toWei(post.changed_price, 'ether')).buildTransaction(
                        {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.signTransaction(tran, real_password)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)

                        os.environ["real_password_eth"+post.user.username] = post.user.address_password
                        test2 = os.getenv("real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(post.user.address),'to': bio.address, 'value': web3.toWei(post.change_value, 'ether')}
                        signed_txn = web3.eth.account.signTransaction(tran, test2)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                        return redirect("eth_to_teen_invoice")
                    else:
                        return redirect("retry_eth_to_teen_trade",time=1)
                else:
                    return redirect("retry_eth_to_teen_trade",time=1)
            else:
                    return redirect("retry_eth_to_teen_trade",time=1)
            
def teen_to_eth(request,id):
    if request.user.is_authenticated:
        post = Trade.objects.filter(id=id).first()
        if request.method == "POST" and post and post.change_currency.name == "Teen" and post.changed_currency.name == "ETH":
            code = request.POST.get("passcode")
            if code:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                    teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                    eth_balanced = float(eth_balanced = float(web3.toWei(web3.eth.getBalance(post.user.address),'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        post.done = "Đã Hoàn Thành Giao Dịch"
                        post.save()

                        os.environ["real_password_teen"+bio.user.username] = bio.address_password
                        real_password = os.getenv("real_password_teen"+bio.user.username)

                        tran = contract.functions.transfer(bio.address, web3.toWei(post.changed_price, 'ether')).buildTransaction(
                        {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.signTransaction(tran, real_password)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)

                        os.environ["real_password_eth"+post.user.username] = post.user.address_password
                        test2 = os.getenv("real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(post.user.address),'to': bio.address, 'value': web3.toWei(post.change_value, 'ether')}
                        signed_txn = web3.eth.account.signTransaction(tran, test2)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                        return redirect("eth_to_teen_invoice")
                    else:
                        return redirect("retry_eth_to_teen_trade",time=1)
                else:
                    return redirect("retry_eth_to_teen_trade",time=1)
            else:
                    return redirect("retry_eth_to_teen_trade",time=1)
            
#transfer_api
def teen_transfer(request,id):
    if request.user.is_authenticated:
        post = Bio.objects.filter(id=id).first()
        if request.method == "POST" and post:
            code = request.POST.get("passcode")
            value = request.POST.get("value")
            if code and value:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                    teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                    eth_balanced = float(eth_balanced = float(web3.toWei(web3.eth.getBalance(post.address),'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        post.done = "Đã Hoàn Thành Giao Dịch"
                        post.save()

                        os.environ["real_password_teen_transfer"+bio.user.username] = bio.address_password
                        real_password = os.getenv("real_password_teen_transfer"+bio.user.username)

                        tran = contract.functions.transfer(post.user.address, web3.toWei(value, 'ether')).buildTransaction(
                        {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.signTransaction(tran, real_password)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                        return redirect("teen_invoice")
                    else:
                        return redirect("retry_teen_transfer",time=1)
                else:
                    return redirect("retry_teen_transfer",time=1)
            else:
                    return redirect("retry_teen_transfer",time=1)
            
def teen_transfer(request,id):
    if request.user.is_authenticated:
        post = Bio.objects.filter(id=id).first()
        if request.method == "POST" and post:
            code = request.POST.get("passcode")
            value = request.POST.get("value")
            if code and value:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(wallet_passcode=final,user=request.user).first()
                    teen_balanced = float(web3.toWei(contract.functions.balanceOf(bio.address).call(),'ether'))
                    eth_balanced = float(eth_balanced = float(web3.toWei(web3.eth.getBalance(post.address),'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        os.environ["real_password_eth"+post.user.username] = post.user.address_password
                        test2 = os.getenv("real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 3000000, 'nonce': web3.eth.getTransactionCount(bio.address),'to': post.address, 'value': web3.toWei(value, 'ether')}
                        signed_txn = web3.eth.account.signTransaction(tran, test2)
                        web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                        return redirect("eth_invoice")
                    else:
                        return redirect("retry_eth_transfer",time=1)
                else:
                    return redirect("retry_eth_transfer",time=1)
            else:
                    return redirect("retry_eth_transfer",time=1)
            
#like_api
def like_post(request,id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
        else:
            post.like.remove(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
    else:
        return redirect("a_login")
    
def like_document(request,id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            return redirect("read_document",id=id)
        else:
            post.like.remove(bio)
            return redirect("read_document",id=id)
    else:
        return redirect("a_login")
    
def like_document(request,id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            return redirect("read_document",id=id)
        else:
            post.like.remove(bio)
            return redirect("read_document",id=id)
    else:
        return redirect("a_login")

def like_gig(request,id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            return redirect("read_gig",id=id)
        else:
            post.like.remove(bio)
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    
def like_question(request,id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            return redirect("read_question",id=id)
        else:
            post.like.remove(bio)
            return redirect("read_question",id=id)
    else:
        return redirect("a_login")

def like_answer(request,id):
    if request.user.is_authenticated:
        post = Answer.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.like:
            post.like.add(bio)
            return redirect("read_question",id=post.question.id)
        else:
            post.like.remove(bio)
            return redirect("read_question",id=post.question.id)
    else:
        return redirect("a_login")
    
#dislike_api
def dislike_post(request,id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
        else:
            post.dislike.remove(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
    else:
        return redirect("a_login")
    
def dislike_document(request,id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            return redirect("read_document",id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_document",id=id)
    else:
        return redirect("a_login")
    
def dislike_document(request,id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            return redirect("read_document",id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_document",id=id)
    else:
        return redirect("a_login")

def dislike_gig(request,id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            return redirect("read_gig",id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    
def dislike_question(request,id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            return redirect("read_question",id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_question",id=id)
    else:
        return redirect("a_login")

def dislike_answer(request,id):
    if request.user.is_authenticated:
        post = Answer.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike:
            post.dislike.add(bio)
            return redirect("read_question",id=post.question.id)
        else:
            post.dislike.remove(bio)
            return redirect("read_question",id=post.question.id)
    else:
        return redirect("a_login")
    
#comment_api
def comment_post(request,id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Post(post=post,user=bio,content=content)
                sql.save()
                sql = Comment_Post.objects.filter(post=post,user=bio,content=content).first()
                goal = "/post/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_post",id=id)
    else:
        return redirect("a_login")
    
def comment_gig(request,id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Gigs(post=post,user=bio,content=content)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Comment_Gigs.objects.filter(post=post,user=bio,content=content).first()
                goal = "/gig/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    
def comment_document(request,id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Document(post=post,user=bio,content=content)
                sql.save()
                
                post.comment_counter += 1
                post.save()

                sql = Comment_Document.objects.filter(post=post,user=bio,content=content).first()
                goal = "/document/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")

def answer(request,id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")
                file = request.FILE.get("file")
                image = request.FILE.get("image")

                sql = Answer(question=post,user=bio,content=content,image=image,file=file)
                sql.save()
                
                post.comment_counter += 1
                post.save()

                sql = Answer.objects.filter(question=post,user=bio,content=content,image=image,file=file,choosen=0).first()
                goal = "/question/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_question",id=id)
    else:
        return redirect("a_login")   

#reply_comment_api
def reply_comment_post(request,id):
    if request.user.is_authenticated:
        post = Comment_Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Post(post=post.post,user=bio,content=content,reply=post)
                sql.save()
                
                post.comment_counter += 1
                post.save()

                sql = Comment_Post.objects.filter(post=post.post,user=bio,content=content,reply=post).first()
                goal = "/post/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_post",id=id)
    else:
        return redirect("a_login")
    
def reply_comment_gig(request,id):
    if request.user.is_authenticated:
        post = Comment_Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Gigs(post=post.post,user=bio,content=content,reply=post)
                sql.save()
                
                post.comment_counter += 1
                post.save()

                sql = Comment_Gigs.objects.filter(post=post.post,user=bio,content=content,reply=post).first()
                goal = "/gig/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    
def reply_comment_document(request,id):
    if request.user.is_authenticated:
        post = Comment_Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method =="POST":
                content = request.POST.get("content")

                sql = Comment_Document(post=post.post,user=bio,content=content,reply=post)
                sql.save()
                
                post.comment_counter += 1
                post.save()

                sql = Comment_Document.objects.filter(post=post.post,user=bio,content=content,reply=post).first()
                goal = "/document/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    
#search_api
def search_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_post",q=q)
    else:
        return redirect("a_login")
    
def search_document(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_document",q=q)
    else:
        return redirect("a_login")
    
def search_gig(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_gig",q=q)
    else:
        return redirect("a_login")

def search_question(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_question",q=q)
    else:
        return redirect("a_login")
    
#update_api
def update_gig(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Gigs.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post':post, "subjects":subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.result = request.POST.get("result")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")
            post.book_include = request.POST.get("book_include")
            post.type_learn = request.POST.get("type_learn")

            post.save()
            return redirect("read_gig",id=id)
    else:
        return redirect("a_login")
    return render("gigs/update.html", context)

def update_document(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Document.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post':post, "subjects":subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")


            post.save()
            return redirect("read_document",id=id)
    else:
        return redirect("a_login")
    return render("document/update.html", context)

def update_question(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Question.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post':post, "subjects":subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")

            post.save()
            return redirect("read_question",id=id)
    else:
        return redirect("a_login")
    return render("question/update.html", context)

def update_answer(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Answer.objects.filter(id=id).first()
        context = {'post':post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")

            post.save()
            return redirect("read_question",id=post.question.id)
    else:
        return redirect("a_login")
    return render("question/answer/update.html", context)

def update_post(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(id=id).first()
        context = {'post':post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/posts/#"+str(id)
            return redirect(goal)
    else:
        return redirect("a_login")
    return render("post/update.html", context)

def update_comment_post(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Post.objects.filter(id=id).first()
        context = {'post':post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/posts/#"+str(post.post.id)
            return redirect(goal)
    else:
        return redirect("a_login")
    return render("post/comment/update.html", context)

def update_comment_gigs(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Gigs.objects.filter(id=id).first()
        context = {'post':post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/gig/"+str(post.post.id)+"/#"+str(id)
            return redirect(goal)
    else:
        return redirect("a_login")
    return render("gigs/comment/update.html", context)

def update_comment_document(request,id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Document.objects.filter(id=id).first()
        context = {'post':post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/document/"+str(post.post.id)+"/#"+str(id)
            return redirect(goal)
    else:
        return redirect("a_login")
    return render("document/comment/update.html", context)

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