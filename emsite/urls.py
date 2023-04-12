from django.urls import path
from . import views

app_name = 'emsite'

urlpatterns = [
        path('',views.index,name='index'),
        path('about/',views.about,name='about'),
        path('services/',views.services,name='services'),
        path('contact/',views.contact,name='contact'),
        path('course_list/',views.course_list,name='course_list'),
        path('course_list/<slug:course>/',views.course_detail,name='course_detail'),
        #path('course_list/<int:id>/',views.course_detail,name='course_detail'),
        path('careers/',views.careers,name='careers'),
        path('leadership_and_mgt_courses/',views.leadership_and_mgt_courses,name='leadership_and_mgt_courses'),
        path('it_courses/',views.it_courses,name='it_courses'),
        path('cloud_and_database/',views.cloud_and_database,name='cloud_and_database'),
        path('404/',views._404,name='404'),
        path('faq/',views.faq,name='faq'),
        path('centers/',views.centers,name='centers'),
        path('blog/',views.post_list,name='post_list'),
        path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,
             name='post_detail'),
        path('<int:post_id>/share/',views.post_share,name='post_share'),
        path('tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
        path('online_form/',views.online_form,name='online_form'),
        path('500/',views._500,name='500')
        #path('feed/',LatestPostsFeed(),name='post_feed'),
        #path('search/',views.post_search,name='post_search'),
        ]