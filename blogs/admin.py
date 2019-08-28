from django.contrib import admin
from  blogs.models import Category,Blog,IndexBlogShow,Images,LogoImage
# Register your models here.
from django.core.cache import cache

class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或则更新表中的数据时候调用'''
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据的时候调用'''
        super().delete_model(request, obj)

        # 发出任务，让celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除缓存
        cache.delete('index_page_data')

class IndexBlogShowAdmin(BaseModelAdmin):
    pass

class ImagesAdmin(BaseModelAdmin):
    pass


class LogoImageAdmin(BaseModelAdmin):
    pass

admin.site.register(Category,BaseModelAdmin)
# admin.site.register(Blog,IndexPromotionBannerAdmin)
admin.site.register(IndexBlogShow,IndexBlogShowAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(LogoImage,LogoImageAdmin)