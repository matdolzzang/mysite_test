from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import loader

from django.http import Http404
from django.urls import reverse

from .models import Question, Choice


# Create your views here.
def index(request):
	#questions = Question.objects.all()
		# str = ''
		# for question in questions:
		# 	str +="{} 날짜 : {} <br/>".format(question.question_txt, question.pub_date)
		# 	str +="-----------------------<br/>"
		# return HttpResponse(str)	
	#context = {'questions': questions}
	#return render(request, 'temp_test/index.html', context) 
	## ㅡ> views 라는 파일에서 우리가 만든 template 을 불러올 수 있구나!!
	## ㅡ> 우리가 temp_test에 만들어 놓은 html 을 rendering 하는 것.

	# latest_question_list = Question.objects.order_by('-pub_date') # - 를 붙여서 최근께 튀어나오도록 
	# output = ', '.join([q.question_txt for q in latest_question_list])
	# return HttpResponse(output)

	 # latest_question_list = Question.objects.order_by('-pub_date')
	 # template = loader.get_template('polls/index.html')
	 # context ={'latest_question_list' : latest_question_list }
	 # return HttpResponse(template.render(context, request)) #ㅡ>템플릿 렌더에서 render 매개변수의 위치 순서
	 ## ---------이렇게 template 을 직접 loader 해도 되더라 -----------------


	'''
지름길: render()¶
template 에 context 를 채워넣어 표현한 결과를 HttpResponse 객체와 함께 돌려주는 구문은 자주 쓰는 용법입니다. 
따라서 Django 는 이런 표현을 쉽게 표현할 수 있도록 단축 기능(shortcuts)을 제공합니다. 
index() view 를 단축 기능으로 작성하면 다음과 같습니다.
	'''

	latest_question_list = Question.objects.order_by('-pub_date')
	context = {'latest_question_list' : latest_question_list}

	# render함수는 request객체를 첫번째 인수로 받고, template이름을 두번째 인자로 사용, 
	# 	세번째 인자는 선택적(optional)인자로 컨텍스트(사전형객체)를 받는다.
	# 	render함수는 HttpResponse객체를 리턴한다.
	return render(request, 'polls/index.html', context) #ㅡ> helloprj 에서 연습했던 것 처럼.



def detail(request, question_id):
	#------------------------------------------------------
	# try:
	# 	question = Question.objects.get(pk = question_id)
	# #except Question.DoesNotExist:	 ## ㅡ> 에러메세지 띄우는 메소드?
	# 	#raise Http404("존재하지 않는 질문 입니다.")
	# except:
	# 	return HttpResponseNotFound("없는 질문 입니다.")	
		
	#-------------------------------------------------------	

	question = get_object_or_404(Question, pk = question_id)
	#get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 
	#몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘깁니다. 
	#약 객체가 존재하지 않을 경우, Http404 예외가 발생합니다.


	#return HttpResponse("당신은 %s번 질문을 보고 있습니다." % question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question':question})
	#return HttpResponse("당신은 %s번 질문의 결과를 보고 있습니다." % question_id)

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
		# POST 데이터 처리가 성공적으로 이루어지면 항상 HttpResponseRedirect를 리턴한다.
		# 이방법을 통해서 유저가 브라우저의 뒤로가기 버튼을 눌렀을 때 데이터가 두번 저장되는 것을 방지할 수 있다.
		# 이방벙법은 장고에만 적용되는 것이아니라, 모든 웹개발에 적용된다.

		# reverse()함수는 뷰의이름과 이뷰를 가리키는 URL패턴의 일부인 변수를 전달 받아서
		# 문자열로 리턴한다. 예> '/polls/4/results/'

	#return HttpResponse("당신은 %s번 질문에 투표를 합니다." % question_id)

# request.POST : 사전과 같은 객체이다.	
# request.POST['choice'] : 선택된 설문의 ID를 문자열로 반환 (request.POST는 항상 문자열로 반환)