# 使用celery
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,redirect,reverse,HttpResponse
from django.template import loader
from django.template import loader,RequestContext

# 在任务处理者一端加上这几句
# django环境的初始化
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_zhou.settings')
django.setup()

from blogs.models import Blog,Category,IndexBlogShow,Images
from django.core.paginator import Paginator


# 创建一个Celery类的实例对象
app=Celery('celery_tasks.tasks',broker='redis://192.168.136.158:6379/8')

@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮箱'''
    subjict = 'www.blogzzhou'
    message = ''
    sender=settings.EMAIL_FROM
    receiver = [to_email]
    html_message = "<h1>嗨！%s,欢迎您来注册我们的博客</h1>请您点击下方链接激活您的账户完成注册<br/><a href='http://127.0.0.1:8000/user/active/%s'>http//:127.0.0.1:8000/user/active/%s</a>"% (
    username, token, token)
    send_mail(subjict,message,sender,receiver,html_message=html_message)


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''

    blogs = IndexBlogShow.objects.all().order_by('index')

    images = Images.objects.all().order_by('-index')
    context = {'blogs': blogs,
               'images':images
               }
    # 使用模板
    temp = loader.get_template('index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')

    with open(save_path,'w') as f :
        f.write(static_index_html)
