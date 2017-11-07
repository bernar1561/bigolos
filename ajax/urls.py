from django.conf.urls import url
from golos.views import *
from golos.models import LikeDislike, Nominees

app_name = 'ajax'
urlpatterns = [
    url(r'^article/(?P<pk>\d+)/like/$', VotesView.as_view(model=Nominees, vote_type=LikeDislike.LIKE),
        name='like'),
    url(r'^article/(?P<pk>\d+)/dislike/$', VotesView.as_view(model=Nominees, vote_type=LikeDislike.DISLIKE),
        name='dislike'),
]