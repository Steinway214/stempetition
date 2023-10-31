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
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="gig_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="gig_like")
    comment_counter = models.IntegerField()

class Comment_Gigs(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
       Bio, related_name='comment_gigs_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Gigs, related_name='comment_gigs', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="gigs_reply")
    
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
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="question_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="question_dislike")
    datetime = models.DateTimeField(auto_now_add=True)
    comment_counter = models.IntegerField()

class Answer(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    file = models.FileField(upload_to="files/",null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="ques_select")
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="question_user_answer")
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name="answer_reply")
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="answer_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="answer_dislike")
    choosen = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    grade = models.IntegerField()
    price = models.FloatField()
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="Document_auth")
    edu_rank = models.ForeignKey(Education_rank,on_delete=models.CASCADE,related_name="doc_edu_rank")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="document_subject")
    file = models.FileField(upload_to="files/",null=True,blank=True)
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="document_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="document_dislike")
    datetime = models.DateTimeField(auto_now_add=True)
    comment_counter = models.IntegerField()

class Comment_Document(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
       Bio, related_name='comment_document_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Document, related_name='comment_document', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="document_reply")
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="comment_document_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="comment_document_dislike")

class Post(models.Model):
    content = models.CharField(max_length=1000)
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="post_like")
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="post_auth")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="post_dislike")
    datetime = models.DateTimeField(auto_now_add=True)
    comment_counter = models.IntegerField()

class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
       Bio, related_name='comment_post_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, related_name='comment_post', on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="post_reply")
    like = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="comment_post_like")
    dislike = models.ManyToManyField(Bio,null=True,blank=True,on_delete=models.CASCADE,related_name="comment_post_dislike")

class payment_method(models.Model):
    name = models.CharField()

    
class Trade(models.Model):
    change_value = models.FloatField()
    changed_value = models.FloatField()
    change_currency = models.ForeignKey(payment_method,on_delete=models.CASCADE,related_name="change_currency")
    changed_currency = models.ForeignKey(payment_method,on_delete=models.CASCADE,related_name="currency")
    payment_method = models.ForeignKey(payment_method,on_delete=models.CASCADE,related_name="payment_method")
    done = models.CharField(max_length=10)
    user = models.ForeignKey(Bio,on_delete=models.CASCADE,related_name="trade_user")
    datetime = models.DateTimeField(auto_now_add=True)


    



