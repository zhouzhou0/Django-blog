# 定义索引类

from haystack import indexes
# 导入模型类
from blogs.models import Blog



# 指定对于某个类的某些数据建立索引
# 索引类名格式，模型类名+Index
class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    # 索要字段, use_template=True指定根据表中哪些字段建立索引文件的说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Blog


    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()