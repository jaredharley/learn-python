from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    # /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # /polls/[id]
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    
    # /polls/[id]/results/
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    
    # /polls/[id]/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)