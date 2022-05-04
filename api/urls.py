from django.urls import path
from api.views import *

urlpatterns = [
    path('match/<int:mid>/<int:pid>', MatchIdPlayerIdStatMin.as_view()),
    path('match/<int:mid>/<int:pid>/', MatchIdPlayerIdStatMin.as_view()),
    # path('match/<int:mid>/<int:pid>', MatchIdPlayerIdStat.as_view())
]