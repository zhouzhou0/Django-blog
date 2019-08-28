# _*_ coding:utf-8 _*_

from datetime import datetime

from django.db import models
from db.base_model import  BaseModel
from user.models import User

# Create your models here.




class Category(models.Model):
    """博客分类"""
    name = models.CharField(verbose_name='文档分类',max_length=20)
    add_time = models.DateTimeField(verbose_name='创建时间',default=datetime.now)
    edit_time = models.DateTimeField(verbose_name='修改时间',default=datetime.now)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tagprofile(models.Model):
    tag_name = models.CharField('标签名', max_length=30)

    class Meta:
        verbose_name = '标签名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class Blog(BaseModel):
    """博客文章"""
    title = models.CharField(verbose_name='博客文章', max_length=50,default='')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,verbose_name='文章分类')
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    # digest = models.TextField(verbose_name='摘要',default='')
    # add_time = models.DateTimeField(verbose_name='创建时间',default=datetime.now)
    # edit_time = models.DateTimeField(verbose_name='更新时间',default=datetime.now)
    read_nums = models.IntegerField(verbose_name='阅读数', default=0)
    conment_nums = models.IntegerField(verbose_name='评论数', default=0)
    # image = models.ImageField(verbose_name='博客封面', upload_to='blog/%Y/%m')
    tag = models.ManyToManyField(Tagprofile)


    class Meta:
        verbose_name = '博客信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Conment(models.Model):
    """对博客评论"""
    user = models.CharField(verbose_name='评论用户', max_length=25)
    title = models.CharField(verbose_name="标题", max_length=100)
    source_id = models.CharField(verbose_name='文章id或source名称', max_length=25)
    conment = models.TextField(verbose_name='评论内容')
    # add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now)
    url = models.CharField(verbose_name='链接', max_length=100)

    class Meta:
        verbose_name = '评论信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class Message(BaseModel):
    """留言"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,verbose_name='用户')
    message = models.TextField(verbose_name='留言')


    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class Images(BaseModel):
    '''首页轮播图片'''

    image = models.ImageField(upload_to='images', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')  # 0 1 2 3

    class Meta:
        db_table = 'df_index_images'
        verbose_name = '首页图片轮播'
        verbose_name_plural = verbose_name

class DaiLiShare(BaseModel):
    '''ip代理分享'''
    ip_address = models.CharField(verbose_name="ip地址", max_length=100)
    port = models.IntegerField(verbose_name='端口', default=0)
    address = models.CharField(verbose_name='服务器地址',max_length=50)
    anonymous=models.CharField(verbose_name='是否匿名',max_length=50)
    type=models.CharField(verbose_name='类型',max_length=50)
    alivetiem=models.CharField(verbose_name='存活时间',max_length=50,null=True)
    vertifytime=models.CharField(verbose_name='验证时间',max_length=50,null=True)

    class Meta:
        db_table = 'df_ip_proxy'
        verbose_name = 'ip代理分享'
        verbose_name_plural = verbose_name


class IndexBlogShow(models.Model):
    blog_id=models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='blog推荐')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_blog_show'
        verbose_name = '首页文章推荐'
        verbose_name_plural = verbose_name


class LogoImage(models.Model):

    image = models.ImageField(upload_to='images', verbose_name='logo')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    class Meta:
        db_table = 'df_logo_images'
        verbose_name = 'logo'
        verbose_name_plural = verbose_name