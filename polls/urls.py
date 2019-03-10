from django.urls import path
from . import views, views_old


# 하나의 project에 여러개의 app을 사용한다면(일반적으로 여러개의 app을 사용함)
# URLconf에 네임스페이스(namespace)를 추가해야 한다. 왜냐하면 Django가 {% url %}태그를 사용하여 어떤 app의
# view에서 URL을 생성해야 하는 지를 알 수 있기 때문이다.

app_name = 'polls'

urlpatterns = [
 	path('', views_old.index),
 	path('<int:question_id>/', views_old.detail, name = 'detail'), # polls/10 
 	path('<int:question_id>/results/', views_old.results, name='results'), #polls/11/results
 	path('<int:question_id>/vote/', views_old.vote, name='vote')
 ]

# name : 각 url 별로 이름을 붙여줍니다. 여기서 정해준 이름은 템플릿 파일에서 사용되니 기억해야한다.

# urlpatterns =[
# 	path('', views.IndexView.as_view(), name='index'),
# 	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
# 	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
# 	path('<int:question_id>/vote/', views.vote, name='vote')
# ]
 #as_views()메소드 : '클래스형 뷰' 를 위한 클래스로 진입하기 위한 메소드 
 # ㅡ> 클래스의 인스턴스를 생성하고, 그 인스턴스의 dispatch() 메소드를 호출
 # ㅡ> dispatch() 메소드는 요청을 검사해 get , post 등의 어떤 http 메소드로 요청되었는지를 알아낸 다음,
 # ㅡ> 인스턴스 내에서 해당 이름을 갖는 메소드로 요청을 중계해준다.