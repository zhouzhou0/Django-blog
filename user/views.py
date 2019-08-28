from django.shortcuts import render,redirect,reverse,HttpResponse
from django.views.generic import View
# Create your views here.
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
import re
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,logout,login
from blogs.models import Blog,Category,LogoImage
from django.core.paginator import Paginator
from django.core.cache import cache



class IndexView(View):
    def get(self,request,page):
        # content = cache.get('all_blog_data')
        # if content is None:
        #     # 设置缓存
        #     print('设置缓存')
        try:
            blogs=Blog.objects.all()
            blogs_index = Blog.objects.all().order_by('-read_nums')[:5]
        except Exception as e:
            return redirect(reverse('user:index'))

        try:
                categorys=Category.objects.all()
        except Exception as e:
            return redirect(reverse('user:index'))

        paginator=Paginator(blogs,3)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        num_pages=paginator.num_pages
        blogs_page=paginator.page(page)
        current_page = paginator.get_page(page)
        logo=LogoImage.objects.get(id=1)
        content={'blogs_page':blogs_page,
                     'num_pages':num_pages,
                     'current_page':current_page,
                     'categorys':categorys,
                     'logo':logo,
                    'blogs_index':blogs_index
                     }
            # cache.set('all_blog_data', content, 3600)
        return render(request,'base.html',content)





# 注册模型类
class RegisterView(View):
    def get(self,request):
        categorys = Category.objects.all()
        blogs_index = Blog.objects.all().order_by('-read_nums')[:5]
        context={
            'categorys':categorys,
            'blogs_index':blogs_index,
        }
        return render(request,'register.html',context)
    def post(self,request):
        ''' 进行注册的处理 '''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        cpassword = request.POST.get('cpwd')
        # 数据的校验
        if not all([username, password, email]):  # all()可以对里面每一个元素进行判断,都为真，返回True
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验两次密码是否一直
        if password != cpassword:
            return render(request, 'register.html', {'errmsg': '两次密码不一样'})

        # 校验用户名是否重复
        try:
            # 用户名存在
            User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        else:
            # 用户存在
            return render(request, 'register.html', {'errmsg': '用户名已经存在'})
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()


        # 发送激活邮件，包含激活链接:/user/active/+id
        # 激活链接中要包含用户的身份信息,并且把身份信息加密

        # 加密用户的身份信息,生成激活的token
        serializer=Serializer(settings.SECRET_KEY,3600)
        serializer=Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token=serializer.dumps(info) #bytes
        token=token.decode()

        # 发邮件
        send_register_active_email.delay(email,username,token)

        # 返回应答,调到首页
        return redirect(reverse('user:login'),{'msg':'请到您输入的邮箱激活账户'})

class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        #进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            token = token.encode()
            info=serializer.loads(token)
            # 获取待激活用户的id
            user_id=info['confirm']
            #根据id获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()

            #跳转到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            #激活链接已经过期
            return HttpResponse('激活链接已经过期')

# 登入模型类
class LoginView(View):
    def get(self,request):
        categorys = Category.objects.all()
        blogs_index = Blog.objects.all().order_by('-read_nums')[:5]
        context={
            'categorys':categorys,
            'blogs_index':blogs_index,
        }
        return render(request,'login.html',context)
    def post(self,request):
        '''登入校验'''
        username=request.POST.get('username')
        password=request.POST.get('pwd')

        #2.进行数据校验
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'请输入完整的用户名和密码'})
        #3. 业务处理 登入校验
        user=authenticate(username=username,password=password)
        if user is not None:
            # 用户名密码正确
                if user.is_active:
                    # 用户激活了
                    login(request,user)
                    # 获取登入后要转跳的地址
                    next_url=request.GET.get('next',reverse('user:index'))
                    # 如果next存在，就跳到next对应地址，否则默认跳到首页
                    response = redirect(next_url)
                    # 返回response
                    return response
                else:
                    # 用户未激活
                    return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# 登出# /user/logout
class LogoutView(View):
    '''用户退出登录'''

    def get(self, request):
        # 清除用户的session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('user:index'))
