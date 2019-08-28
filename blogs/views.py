from django.shortcuts import render,redirect,reverse,HttpResponse
from django.views.generic import View
# Create your views here.
from utils.mixin import LoginrequiredMixin
from blogs.models import Blog,Category,DaiLiShare,IndexBlogShow,Images,LogoImage
from user.models import User
from django.core.paginator import Paginator
from django.core.cache import cache


class UserView(LoginrequiredMixin,View):
    def get(self,request):
        categorys = Category.objects.all()
        content={'categorys':categorys}
        return render(request,'user_center.html',content)

    def post(self,request):

        title = request.POST.get('title')
        gcontent = request.POST.get('gcontent')
        category = request.POST.get('category')
        user = request.user
        # user = User.objects.get(username=user)
        id=user.id
        print(title,id,gcontent)
        if not all((title, gcontent)):
            return render(request, 'user_center.html', {'errmsg': '数据不完整'})
        blog=Blog()
        blog.title=title
        blog.content=gcontent
        user = User.objects.get(username=user)
        blog.author=user
        category=Category.objects.get(name=category)
        blog.category=category
        # blog=Blog.objects.create(
        #         title=title,
        #         # category=category,
        #         author=id,
        #
        #     )
        blog.save()
        return redirect(reverse('blogs:personal_center'))

class Personal_Blogs_list(LoginrequiredMixin,View):
    def get(self,request,page):
        user=request.user
        user=User.objects.get(username=user)
        # blogs=user.Blog_set.all()
        categorys=Category.objects.all()
        try:
            blogs = Blog.objects.filter(author_id=user.id)
        except Exception as e:
            return redirect(reverse('blogs:pblogs'))

        paginator = Paginator(blogs, 5)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        num_pages=paginator.num_pages

        # 获取第page页的Page实例对象
        blogs_page = paginator.page(page)
        current_page=paginator.get_page(page)
        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页码小于5页，显示所以页码
        # 2.如果当前页是前3页，显示1-5页
        # 3. 如果当前页是后3页，显示后5页
        # 4.其他情况显示当前页的前两页,当前页，当前页的后2页
        # # num_pages =paginator.num_pages
        # if num_pages < 5:
        #         pages= range(1,num_pages)
        # elif page <= 3:
        #     pages = range(1,6)
        # elif num_pages-page <= 2:
        #     pages=range(num_pages-4,num_pages+1)
        # else:
        #     range(page-2,page+3)


        content = {'categorys': categorys,
                   'blogs_page': blogs_page,
                   'blogs': blogs,
                    'num_pages':num_pages,
                   'current_page':current_page,
                   }

        return render(request,'personal_blogs_list.html',content)

#/detail
class DetailView(View):
    '''文章详情页'''
    def get(self,request,blog_id):
        try:
            blog =Blog.objects.get(id=blog_id)
            blog.read_nums +=1
            blog.save()
        except Blog.DoesNotExist:
            return redirect(reverse('user:index'))
        categorys = Category.objects.all()

        content={'blog':blog,'categorys':categorys}
        return render(request,'detail.html',content)


class BlogTypeView(View):
    def get(self,request,page):
        type_id=request.GET.get('type_id')
        try:
            type=Category.objects.get(id=type_id)
        except Category.DoesNotExist:
            return redirect(reverse('user:index'))
        blogs=Blog.objects.filter(category=type.id)
        paginator=Paginator(blogs,5)

        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        blogs_page=paginator.page(page)
        num_pages=paginator.num_pages
        current_page=paginator.get_page(page)

        content ={'blogs':blogs,
                  'blogs_page':blogs_page,
                  'num_pages':num_pages,
                  'current_page':current_page
                  }
        return render(request,'blog_sort.html',content)


class ProxyView(View):
    ''''''
    def get(self,request,page):
        proxis=DaiLiShare.objects.all()
        paginator = Paginator(proxis, 10)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        proxis_page=paginator.page(page)
        num_pages=paginator.num_pages
        current_page=paginator.get_page(page)
        categorys = Category.objects.all()

        content={'proxis_page':proxis_page,
                 'num_pages':num_pages,
                 'current_page':current_page,
                 'categorys':categorys
                 }
        return render(request,'proxy.html',content)


class StaticIndex(View):
    def get(self,request):
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')
        if context is None:
            print('设置缓存')
            # 缓存中没有数据
            # logo=LogoImage.objects.get(id=1)
            blogs=IndexBlogShow.objects.all().order_by('index')
            images=Images.objects.all().order_by('-index')
            categorys = Category.objects.all()
            blogs_index = Blog.objects.all().order_by('-read_nums')[:5]

            context={'blogs':blogs,
                 'images':images,
                 # 'logo':logo,
                     'categorys':categorys,
                     'blogs_index':blogs_index,
                 }
            # 设置缓存
            # key value 过期时间
            cache.set('index_page_data',context,3600)
        return render(request, 'index.html', context)

