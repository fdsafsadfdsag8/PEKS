from django.db import models
# 数据库表的布局，再附加一些元数据
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=128, unique=True) # 必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
    password = models.CharField(max_length=256) # 必填，最长不超过256个字符
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self): # 帮助人性化显示对象信息；
        return self.name

    # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"