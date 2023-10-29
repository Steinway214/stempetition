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
    wallet_passcode = models.TextField()
    edu_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="user_edu_rank")
    avatar = models.ImageField(upload_to="images/",null=True,blank=True)
    thumnail = models.ImageField(upload_to="images/",null=True,blank=True)


class Subject(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    schoolable = models.IntegerField()


class Gigs(models.Model):
    title = models.CharField()
    description = models.TextField()
    result = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    education_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="Education_rank")
    grade = models.IntegerField()
    price = models.FloatField()
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="subject_choose")
    user = models.ForeignKey(Bio, on_delete=models.CASCADE, related_name="gigs_auth")
    book_include = models.CharField(max_length=1000)
    type_learn = models.CharField(max_length=1000)
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)

class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
       Bio, related_name='comment_gigs_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Gigs, related_name='comment_gigs', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="post_reply")
    
class join_cls(models.Model):
    gig = models.ForeignKey(Gigs,on_delete=models.CASCADE,related_name="joined_gig")
    student =  models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="student_join")

class Learn(models.Model):
    check_stu = models.ForeignKey(join_cls,on_delete=models.CASCADE,related_name="check_stu")
    cls_day = models.IntegerField()
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
    price = models.FloatField()
    like = models.ManyToManyField(Bio)
    dislike = models.ManyToManyField(Bio)
    datetime = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    file = models.FileField(upload_to="files/",null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="ques_select")
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="question_user_answer")
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="answer_reply")
    upvote = models.ManyToManyField(Bio)
    downvote = models.ManyToManyField(Bio)
    choosen = models.IntegerField()
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

class Post(models.Model):
    content = models.CharField(max_length=1000)
    like = models.ManyToManyField(Bio)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="post_auth")
    dislike = models.ManyToManyField(Bio)
    datetime = models.DateTimeField(auto_now_add=True)

class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
       Bio, related_name='comment_post_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, related_name='comment_post', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="post_reply")

class payment_method(models.Model):
    name = models.CharField()

    
class Trade(models.Model):
    value = models.FloatField()
    payment_method = models.ForeignKey(payment_method)
    done = models.CharField(max_length=10)
    datetime = models.DateTimeField(auto_now_add=True)


    



