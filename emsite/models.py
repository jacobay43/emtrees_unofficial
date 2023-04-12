from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=800)
    content = models.TextField()
    course_for = models.CharField(max_length=800) #redirect to a form prefilled with this course
    img_for = models.CharField(max_length=800)
    tags = TaggableManager()
    def __str__(self):
        return self.title
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
class Post(models.Model):
    STATUS_CHOICES = (
            ('draft','Draft'),
            ('published','Published'),
            )
    title = models.CharField(max_length=800)
    slug = models.SlugField(max_length=800,unique_for_date='publish')
    author_name = models.CharField(max_length=800)
    post_image = models.ImageField(upload_to='posts',blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return f'Blog "{self.title}"'
    def get_absolute_url(self):
        return reverse('emsite:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
class Service(models.Model):
    icon_string = models.CharField(max_length=800)
    title = models.CharField(max_length=800)
    body = models.TextField()
    def __str__(self):
        return f'Service: "{self.title}"'
class Course(models.Model):
    title = models.CharField(max_length=800)
    description = models.TextField()
    details = models.TextField()
    slug = models.SlugField(max_length=250,blank=True)
    image1 = models.ImageField(upload_to='course1',blank=True)
    image2 = models.ImageField(upload_to='course2',blank=True)
    image3 = models.ImageField(upload_to='course3',blank=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    def __str__(self):
        return f'Course: "{self.title}"'
    def get_absolute_url(self):
        return reverse('emsite:course_detail',args=[self.slug])
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Course,self).save(*args,**kwargs)
class Contact(models.Model):
    name = models.CharField(max_length=400)
    email = models.EmailField(max_length=400)
    phone_number = models.CharField(max_length=400)
    message = models.TextField()
    def __str__(self):
        return f'Submission from {self.name}'
class OnlineForm(models.Model):
    name = models.CharField(max_length=1200)
    course_name = models.CharField(max_length=1200)
    phonenum = models.CharField(max_length=1200)
    email = models.EmailField()
    state = models.CharField(max_length=1200)
    country = models.CharField(max_length=1200)
    prof_creds = models.CharField(max_length=1200,blank=True,default='')
    proposed_info = models.TextField()
    class Meta:
        verbose_name_plural = 'forms'
    def __str__(self):
        return self.name