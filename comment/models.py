from django.db import models
import threading
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# 多线程处理发送邮件的方法
class SendEmial(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, 
                  '', 
                  settings.EMAIL_HOST_USER, 
                 [self.email], 
                 fail_silently=self.fail_silently,
                 html_message=self.text
                 )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name= '评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name= '评论时间')
    comment_user =models.ForeignKey(User, related_name='comments', on_delete= models.CASCADE, verbose_name='评论者')

    # 创建一个字段来记录一条评论下的所有回复
    top = models.ForeignKey('self', related_name= 'top_comment', null= True, on_delete= models.CASCADE, verbose_name='品论这条')
    # 回复功能的字段名,使用related_name来解决关联两个外键的冲突的方法
    parent = models.ForeignKey('self', related_name= 'paren_comment', null= True, on_delete= models.CASCADE, verbose_name= '品论这条')
    reply_to = models.ForeignKey(User, related_name='replies', null= True, on_delete= models.CASCADE, verbose_name='回复者')

    def __str__(self):
        return self.text
        
     # 发送邮件
    def send_email(self):
        # 评论发送邮件
        if self.parent is None:
            # 评论博客
            subject = '博客有新的评论'
            email = self.content_object.get_email()
        else:
            subject = '有新的回复'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment.text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_email', context)
            send_emial = SendEmial(subject,text,email)
            send_emial.start()

    class Meta:
        ordering = ['comment_time']