from django.db import models
from django.contrib.auth.models import User


class Education_rank(models.Model):
    name = models.CharField()
    

class Bio(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField()
    facebook = models.CharField(max_length=1000,null=True,blank=True)
    instagram = models.CharField(max_length=1000,null=True,blank=True)
    twitter = models.CharField(max_length=1000,null=True,blank=True)
    zalo = models.CharField(max_length=1000,null=True,blank=True)
    grade = models.IntegerField()
    address = models.TextField()
    address_password = models.TextField()
    wallet_passcode = models.CharField(max_length=6)
    edu_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="user_edu_rank")
    avatar = models.ImageField(upload_to="images/",null=True,blank=True)
    thumnail = models.ImageField(upload_to="images/",null=True,blank=True)


class Subject(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    schoolable = models.IntegerField()

class Comment_gigs(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="comment_gigs_reply")

class Gigs(models.Model):
    title = models.CharField()
    description = models.TextField()
    result = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    education_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="Education_rank")
    grade = models.IntegerField()
    book_include = models.CharField(max_length=1000)
    type_learn = models.CharField(max_length=1000)
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)
    comment = models.ForeignKey(Comment_gigs,on_delete=models.CASCADE,related_name="comment_gigs")

class Answer(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    file = models.FileField(upload_to="files/",null=True,blank=True)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="question_user_answer")
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="answer_reply")
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)
    choosen = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    title = models.CharField()
    description = models.TextField()
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="question_user_answer")
    file = models.FileField(upload_to="files/",null=True,blank=True)
    subject = models.ForeignKey(Subject)
    education_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="Education_rank_question")
    grade = models.IntegerField()
    price = models.IntegerField()
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="answer")
    datetime = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    grade = models.IntegerField()
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="Document_auth")
    edu_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="doc_edu_rank")
    file = models.FileField(upload_to="files/",null=True,blank=True)
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)
    datetime = models.DateTimeField(auto_now_add=True)

class Comment_post(models.Model):
    content = models.CharField(max_length=1000)
    user = user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="comment_post_auth")
    datetime = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="comment_post_reply")

class Post(models.Model):
    content = models.CharField(max_length=1000)
    comment = models.ForeignKey(Comment_post,on_delete=models.CASCADE,related_name="comment_post")
    like = models.ManyToManyField(Bio)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="post_auth")
    dislike = models.ManyToManyField(Bio)
    datetime = models.DateTimeField(auto_now_add=True)
    


    



