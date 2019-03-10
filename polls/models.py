import datetime
from django.db import models
from django.utils import  timezone
# 여기에 정의된 모델(데이터베이스 테이블)은 migrate명령을 이용하여
# 실제 데이터베이스에 적용할 수 있다.
'''
본질적으로, 모델이란?
부가적인 메타데이터를 가진 데이터베이스의 구조(layout)를 말합니다.
'''

# migrate 사용 순서
# 모델을 변경(models.py)
# python manage.py makemigrations <앱명> (변경사항에 대한 migration을 만들기)
# python manage.py migrate (데이터베이스에 적용) 
'''

'''

# 참고로 sql을 확인하기 위해서는 sqlmigrate 명령을 이용한다.
'''
class <모델명>  ( ex_ Question)
     필드명(ex_ pub_data ) 
'''

# Create your models here.
class Question(models.Model): 
	question_txt = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	'''
	__str__ : 
	인스턴스 자체를 출력 할 때의 형식을 지정해주는 함수
	'''
	def __str__(self):
		return self.question_txt

	def published_recently(self):
		return self.pub_date >= timezone.now()-datetime.timedelta(days = 1)
		# 객체를 통해 클래스의 메서드를 호출하려면 a.setdata(4, 2) 와 같이 도트(.) 연산자를 이용해야 한다.
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	# ㅡ> 서로 두개의 테이블을 연관 시킬 때.(위의 Question)
	# ex) 사원(부서코드) , 부서(부서코드 - 부서명)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default = 0)
 
	def __str__(self):
		return self.choice_text
'''
 각 모델은 django.db.models.Model 이라는 클래스의 
 서브클래스로 표현됩니다. 
 각 모델은 몇개의 클래스 변수를 가지고 있으며, 
 각각의 클래스 변수들은 모델의 데이터베이스 필드를 나타냅니다.
 데이터베이스의 각 필드는 Field 클래스의 인스턴스로서 
 표현됩니다. 
 CharField 는 문자(character) 필드를 표현하고, 
 DateTimeField 는 날짜와 시간(datetime) 필드를 표현합니다. 이것은 각 필드가 어떤 자료형을 가질 수 있는지를 Django 에게 말해줍니다.
 
 몇몇 Field 클래스들은 필수 인수가 필요합니다. 
 예를 들어, CharField 의 경우 
 max_length 를 입력해 주어야 합니다. 
 이것은 데이터베이스 스키마에서만 필요한것이 아닌 
 값을 검증할때도 쓰이는데, 곧 보게 될것입니다.

 또한 Field 는 다양한 선택적 인수들을 가질 수 있습니다. 
 이 예제에서는, default 로 하여금 votes 의 기본값을 0 으로
 설정하였습니다.

 마지막으로, ForeignKey 를 사용한 관계설정에 대해 
 설명하겠습니다. 이 예제에서는 각각의 Choice 가 하나의 
 Question 에 관계된다는 것을 Django 에게 알려줍니다.
  Django 는 다-대-일(many-to-one), 다-대-다(many-to-many)
  일-대-일(one-to-one) 과 같은 
  모든 일반 데이터베이스의 관계들를 지원합니다.
 '''


# Django 모델 API (데이터를 추가/갱신/조회)
# insert : 객체생성후에 save() 함수를 이용하여 새객체를 insert한다.
# select : Django 모델 클래스에 대해 objects라는 Manager 객체를 자동으로 추가한다.
	# objects는 django.db.models.Manager 이다. 이매니저 객체를 이용해서 데이터
	# 필터링 할 수 있고, 정렬을 할 수 있으며 기타 여러 기능들을 사용할 수 있다.
	# 데이터를 읽어올 때 바로 이 매니저 객체를 사용하였음(모델클래스.objects)
	# all() : 테이블 데이터를 모두 가져온다. Question.objects.all() 
	# filter() : 특정조건을 이용하여 Row들을 가져오기 위한 메소드
	# exclude() : 특정 조건을 제외한 나머지 Row들을 가져오기 위한 메소드 filter()반대개념
	# ㅡㅡ> Quertset 을 가져오는 얘들. 
	# get() : 하나의 row만을 가져올 때 사용하는 메소드이다. Primary Key를 가져올때
	# 는 Question.objects.get(pk = 1)
	
	# count() : 데이터의 갯수(row 수)를 세기위한 메소드
	# order_by() : 데이터를 특정 키에 따라 정렬하기 위한 메소드, 정렬키를 인수로 사용하는데
		# -가 붙으면 내림차순이 된다.
		# Question.objects.order_by('-id')
	# distinct() : 중복된 값은 하나로만 표시하기 위한 메소드, SQL의 SELECT DISTINCT와 같은
		# 같은 기능
		# rows = User.objects.distinct('name')
	# first() : 여러개의 데이터중에서 처음에 있는 row만을 리턴한다. 
		# Type : <class 'polls.models.Question'>
		# rows = User.objects.order_by('name').first()
		# ex) Question.objects.order_by().first()
		# 위의 결과는 정렬된 레코드(row)중에서 가장 첫번째 row가 리턴값이 된다.
	# last() : 여러개의 데이터중에서 마지막 row만을 리턴한다.
	
	## 위의 메소드들은 실제 데이터 결과를 직접 리턴하기보다는 쿼리 표현식(QuersySet)으로
	## 리턴한다.따라서, 여러 메소드들을 체인처럼 연결해서 사용할 수 있다.
	## row = User.objects.filter(name = 'Lee').order_by('-id').first()		

# update : 수정할 row객체를 얻은 후에 변경할 필드를 수정한다. 수정한 후에는 save() 메소드를
	# 호출한다. SQL의 UPDATE가 실행되어 테이블에 데이터가 갱신된다.

# delete : Row객체를 얻어온 후에 delete() 메소드를 호출한다. delete메소드에 의해서
	# 바로 데이터베이스의 레코드(row)가 삭제된다.	