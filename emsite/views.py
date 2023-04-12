from django.shortcuts import render, get_object_or_404
from .models import Course, Post, Article
from .forms import ContactForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, OnlineFormToFill
from django.core.mail import send_mail, BadHeaderError
from taggit.models import Tag

#:TODO Add close functionality to messages popup on submissions
#:TODO Add Modern Website Footer like that in Blender website
#:TODO Fix Stretch in Carousel in index page

def index(request):
    articles = Article.objects.all()[:3]
    return render(request,'emsite/index.html',{'articles':articles})
def about(request):
    return render(request,'emsite/about.html')
def services(request):
    return render(request,'emsite/services.html')
def contact(request): 
    if request.method != 'POST':
        form = ContactForm()
    else:
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Message sent!')
            return HttpResponseRedirect(reverse('emsite:contact'))
        else:
            messages.error(request,'Error sending message')
    context = {'form':form}
    return render(request,'emsite/contact.html',context)
def course_list(request):
    all_courses = Course.objects.all()
    paginator = Paginator(all_courses,3) #show 3 courses per page
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        #if req page is out of range...
        courses = paginator.page(paginator.num_pages)
    return render(request,'emsite/portfolio-1-col.html',{'page':page,
                                                         'courses':courses})
def course_detail(request,course):
    course = get_object_or_404(Course,slug=course)
    course_tags_ids = course.tags.values_list('id',flat=True)
    similar_courses = Course.objects.filter(tags__in=course_tags_ids)
    similar_courses = similar_courses.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    return render(request,'emsite/portfolio-item.html',{'course':course,
                                                        'similar_courses':similar_courses})
def careers(request):
    return render(request,'emsite/careers.html')
def leadership_and_mgt_courses(request):
    PMP = Course.objects.get(title="Project Management")
    course_tags_ids = PMP.tags.values_list('id',flat=True)
    similar_courses = Course.objects.filter(tags__in=course_tags_ids)
    similar_courses = similar_courses.annotate(same_tags=Count('tags')).order_by('-same_tags')
    paginator = Paginator(similar_courses,3) #show 3 courses per page
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        #if req page is out of range...
        courses = paginator.page(paginator.num_pages)
    return render(request,'emsite/lead-mgt-courses.html',{'page':page,
                                                    'courses':courses})
def it_courses(request):
    NETWORKING = Course.objects.get(title="Networking")
    course_tags_ids = NETWORKING.tags.values_list('id',flat=True)
    similar_courses = Course.objects.filter(tags__in=course_tags_ids)
    similar_courses = similar_courses.annotate(same_tags=Count('tags')).order_by('-same_tags')
    paginator = Paginator(similar_courses,3) #show 3 courses per page
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        #if req page is out of range...
        courses = paginator.page(paginator.num_pages)
    return render(request,'emsite/it-courses.html',{'page':page,
                                                    'courses':courses})
def cloud_and_database(request):
    CLOUD = Course.objects.get(title="Cloud Computing")
    course_tags_ids = CLOUD.tags.values_list('id',flat=True)
    similar_courses = Course.objects.filter(tags__in=course_tags_ids)
    similar_courses = similar_courses.annotate(same_tags=Count('tags')).order_by('-same_tags')
    paginator = Paginator(similar_courses,3) #show 3 courses per page
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        #if req page is out of range...
        courses = paginator.page(paginator.num_pages)
    return render(request,'emsite/cloud-computing-and-database-courses.html',{'page':page,
                                                    'courses':courses})

def _404(request):
    return render(request,'404.html')

def _500(request):
    return render(request,'500.html')

def faq(request):
    return render(request,'emsite/faq.html')

def centers(request):
    return render(request,'emsite/test-assessment-centers.html')


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
def post_list(request,tag_slug=None):
    tag = None
    object_list = Post.published.all()
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list,3) #3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range,deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,
                             publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    #similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/post/detail.html',{'post':post,
                                                   'comments':comments,
                                                   'new_comment':new_comment,
                                                   'comment_form':comment_form,
                                                   'similar_posts':similar_posts})
def post_share(request,post_id):
    #retrieve post by id
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            #send mail:
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            try:
                send_mail(subject, message, 'jacobay43@gmail.com',[cd['to']])
            except BadHeaderError:
                return HttpResponse('Invalid Header found.')
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

def online_form(request): 
    if request.method != 'POST':
        form = OnlineFormToFill()
    else:
        form = OnlineFormToFill(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Form submitted successfully! You will be contacted soon.')
            return HttpResponseRedirect(reverse('emsite:online_form'))
        else:
            messages.error(request,'Error submitting form')
    context = {'form':form}
    return render(request,'emsite/online_form.html',context)