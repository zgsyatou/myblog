from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.core.cache import cache
from ReadCount.tool  import get_sever_day_read, get_one_day_hot, get_yesterday_hot, get_berfor_seven_day_hot
from blog.models import Blog

def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_sever_day_read(blog_content_type)

# 获取七天的博客访问数据的缓存
    seven_berfor_cache = cache.get('seven_berfor_cache')
    if seven_berfor_cache is None:
        seven_berfor_cache = get_berfor_seven_day_hot()
        cache.set('seven_berfor_cache', seven_berfor_cache, 3600)
    else:
        print('use cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['one_day_hot'] = get_one_day_hot(blog_content_type)
    context['yesterday_hot'] = get_yesterday_hot(blog_content_type)
    context['seven_day_hot'] = seven_berfor_cache
    return render(request,  'index.html',context)
