"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import sys
from django.contrib import admin
from django.urls import path, include
from search_kw import views

print(sys.path)

urlpatterns = [ # 除了admin路由外，尽量给每个app设计自己独立的二级路由。
    # path('search_kw/', include('search_kw.urls')), # include语法相当于多级路由，它把接收到的url地址去除与此项匹配的部分，将剩下的字符串传递给下一级路由urlconf进行判断
    # path(r'^call/$', include('search_kw.urls')),
    path('index2/', views.index2),
    path('index_new/', views.index_new),
    path('login/', views.login),
    path('register/', views.register),
    path('signup2/', views.signup2),
    path('search2/', views.search2),
    path('sendRcv2/', views.sendRcv2),
    path('search2/', views.search2),
    path('search_test/', views.search_test),
    path('admin/', admin.site.urls),
    path('index/', views.index),
]
