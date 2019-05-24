from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from posts.forms import PostForm,AvaForm,UsrForm,PhForm,SigForm,QqForm,MaForm
from posts.models import Post,Category,Like,Favorite,Tag,Transmit
from users.models import User
from comments.models import Comment
from comments.forms import CommentForm
import datetime
import json
from comments.models import CommentReply
from hotinfo.models import HotInfo
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests
from lxml import html
today = datetime.date.today()
year = today.year
month = today.month
day = today.day
week = today.weekday()

startdate = datetime.date(year,month,day-week-2)
enddate = datetime.date(year,month,day+week)


# Create your views here.

def index(request):
    # url = 'http://yz.chsi.com.cn/kyzx/kydt/'  # 目标网址
    # page = requests.get(url)  # 获取网页对象
    # sector = html.etree.HTML(page.text)  # html解析
    # info = sector.xpath('//div[@class="content-l"]/ul/li/a//text()')  # 查找标题
    # link = sector.xpath('//div[@class="content-l"]/ul/li/a/@href')  # 对应的链接
    # base_url = 'http://yz.chsi.com.cn'
    # target_link = []  # 我们需要的网址信息
    # for i in link:
    #     res = base_url + i
    #     target_link.append(res)
    # print(target_link)
    #
    # ### 转化json 存到数据库
    # res = [dict(title=info[index], link=target_link[index]) for index in range(len(info))]
    # print(res)
    # res2 = [dict(model='hotinfo.hotinfo', fields=k) for k in res]
    # print(res2)
    #
    # for index in range(len(info)):
    #     try:
    #         hotinfo = HotInfo()
    #         hotinfo.title = info[index]
    #         hotinfo.link = target_link[index]
    #         hotinfo.save()
    #     except Exception as e:
    #         print(e)
    #
    # # json_str2 = json.dumps(res2,ensure_ascii=False)
    # # print ("python原始数据：", repr(res2))
    # # print ("json对象：", json_str2,type(json_str2))
    #
    # with open("./bbstest.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(res2, json_file, ensure_ascii=False)
    return render(request, 'posts/index2.html', {})


class IndexView(ListView):
    global year, month, day, week, startdate, enddate
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        hot_list = Post.objects.all().order_by('-views')[0:8]  # 热点信息
        hotinfo = HotInfo.objects.all()[0:10]
        timeweek = Post.objects.filter(created_time__range=(startdate, enddate)).order_by('-views')
        timemonth = Post.objects.filter(created_time__month=month).order_by('-views')[0:8]
        timeday = Post.objects.filter(created_time__day=day).order_by('-views')
        print(context)
        context.update({'hot_list': hot_list, 'hotinfo': hotinfo, 'timeweek': timeweek, 'timemonth': timemonth,
                        'timeday': timeday})
        return context

def posts(request):
    post_list = Post.objects.all().order_by('-create_time')
    hot_list = Post.objects.all().order_by("-views")
    return render(request,'posts/index.html',locals())

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reply_list = CommentReply.objects.all()
    hot_list = Post.objects.all().order_by('-views')[0:8]
    post.increase_views()
    form = CommentForm()
    comment_list = post.comment_set.all().order_by('-created_time')
    avt = []
    if len(comment_list) > 0:
        for comment in comment_list:
            com_id = comment.id
            q = {
                'id': com_id,
                'post_id': pk,
            }
            com_list = Comment.objects.filter(**q)
            if len(com_list) > 0:
                for com in com_list:
                    userid = com.user_id
                    userobj = User.objects.get(id = userid)
                    avt.append(userobj)
    print(avt,type(avt))
    return render(request, 'posts/detail3.html', locals())

def categories(request, pk):
    # 根据pk取得category对象db
    category = get_object_or_404(Category, pk=pk)
    # 根据取得category来正向查找post
    # post_list = Post.objects.filter(category=category)
    # 反向查
    post_list = category.post_set.all()
    return render(request, 'posts/index.html', locals())


def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    # 反向查
    post_list = tag.post_set.all()
    return render(request, 'posts/index.html', {'post_list': post_list})

@login_required
def add_post(request):        # 发帖

    post_list = Post.objects.all().order_by('-created_time')
    hot_list = Post.objects.all().order_by("-views")[0:8]
    form = PostForm(instance=request.user)
    # 判断request的请求方法，如果是post方法，那么就处理数据
    if request.method == 'POST':
        # 获取前台传过来的数据，用来生成form对象
        form = PostForm(request.POST)

        # 判断form表单数据是否合法
        if form.is_valid():
            post = form.save(commit=False)
            # 如果合法，则保存数据
            post.author=request.user
            form.save()
            # print(form.cleaned_data)
            post_list = Post.objects.all().order_by('-created_time')
            return render(request,'posts/index.html', {'post_list': post_list})
            # return HttpResponse("{'status':'success'}", content_type='application/json')
            # messages.success(request, '保存成功！')
            # return HttpResponseRedirect('/index')
    return render(request, 'posts/add.html', locals())

@login_required
def profile(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    post_list = user.post_set.all()
    return render(request, 'posts/profile.html',locals())

def like(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.like_set.all()
    return render(request, 'posts/profile.html',locals())

def favorite(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.favorite_set.all()

    return render(request, 'posts/profile.html',locals())


def transmite(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.transmit_set.all()

    return render(request, 'posts/profile.html',locals())

def comment(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.comment_set.all()
    return render(request, 'posts/profile.html',locals())

@login_required
def add_favorite(request):
    print('hello')
    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        print(contentid[0])
        post = Post.objects.get(id=contentid[0])
        print(post)
        created_time = datetime.datetime.now()
        post_id = Favorite.objects.filter(post_id=post)
        print(post_id)
        if post_id.exists():
            resp = {'status': '已经收藏'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        else:
            post.favo_num +=1
            post.save()
            Favorite.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '收藏成功'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def add_like(request):
    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        post = Post.objects.get(id=contentid[0])
        created_time = datetime.datetime.now()
        post_id = Like.objects.filter(post_id=post)
        if post_id.exists():
            resp = {'status': '已经点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            post.like_num +=1
            post.save()
            Like.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '成功点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def add_transmit(request):      # 转发
    path = request.path
    user = request.user
    post = Post.objects.all()

    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        post = Post.objects.get(id=contentid[0])

        post.save()

        created_time = datetime.datetime.now()
        post_id = Transmit.objects.filter(post_id=post)
        if post_id.exists():
            resp = {'status': '已转发'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            post.transmit_num += 1
            post.save()
            post.id = None  # 只需要改变新对象的主键值，然后运行save() 复制数据库
            post.post_from += 1
            post.views = 0
            post.save()
            Transmit.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '成功转发'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'posts/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(content_html__icontains=q))
    return render(request, 'posts/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})