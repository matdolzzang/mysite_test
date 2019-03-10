from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

'''
1. 각 제너릭 뷰는 어떤 '모델'이 적용될 것인지를 알아야합니다. 이것은 model 속성을 사용하여 제공됩니다.
2. DetailView 제너릭 뷰는 URL에서 캡쳐 된 기본 키 값이 "pk"라고 기대하기 때문에 
question_id를 제너릭 뷰를 위해 pk로 변경합니다.(polls/url.py ㅡ> urlpattern)
'''
# template_name 속성 :
# ㅡ> Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용됩니다

# ListView 제네릭 뷰는 <app name>/<model name>_list.html 템플릿을 기본으로 사용합니다
class IndexView(generic.ListView):
	model= Question
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	'''
	그러나 ListView의 경우 자동 생성 된 컨텍스트 변수는 question_list 입니다. 
	이것을 덮어 쓰려면 context_object_name 속성을 제공하고, 
	대신에 latest_question_list를 사용하도록 지정하십시오
	'''

	# ListView에서 자동 생성되는 컨텍스트 변수는 <mdoel_name>_list 인다. 여기서 말하는 object는
	# question 이다. 따라서 자동 생성되는 컨텍스트 변수는 question_list 이다.
	# context_object_name 속성을 이용하여 오버라이딩 해준다.
	#context_object_name = 'latest_question_list'
	#model = Question
	def get_queryset(self):
		return Question.objects.order_by('-pub_date')

# 기본적으로 DetailView 제너릭 뷰는 <app name>/<model name>_detail.html 템플릿을 사용합니다
# ex ) "polls/question_detail.html"

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	# DetailView에서도 모델이 Question 이기 때문에 Django에서는 컨텍스트 변수의 이름을 question으로 결정
	# 한다. 


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html',{
			'question':question,
			'error_message': "선택 에러 입니다.",
			})
	else:
		selected_choice.votes += 1	
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
