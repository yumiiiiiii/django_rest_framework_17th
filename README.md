# CEOS 17기 백엔드 스터디

---
외부 데이터베이스는 처음 써봐서 신기했다. shell에서 데이터베이스를 열고 django-admin 페이지에 가지 않아도 데이터를 가지고 활용할 수 있어 편리했다.
데이터를 다루는 여러 명령어가 있는데, 이중에서 내가 지금 쓸 수 있는 것들로만 사용해봤다.
- 모델명.objects.all() : 모델의 모든 객체 조회
- 모델명.object.create(필드=필드값, ...) : 모델 객체 생성, 모델 옵션들에 주의!!
- 모델명.object.get(필드=필드값) : 모델 값 반환, 하나의 값만 반환한다.
- 모델명.object.filter(필드=필드값) : 모델 값 검색!
아래는 활용 결과들
1. user를 만들고, 그에 맞는 profile을 만들었다. post 객체가 user가 아닌 이를 상속받는 profile을 참조하기 때문에...만들어야함.
![orm user,profile 만들기](./images/orm user,profile 만듥.png)
2. me라는 변수에 profile을 저장하고, 이를 이용해 post 객체를 만들었다.
![orm me에 profile저장, post 생성](./images/orm me에 profile저장, post생성.png)
3. filter기능을 활용했다. 일부만 검색해도 일치하면 다 나오도록 만들고 싶었는데, 그렇게 하려면 django에서 제공하는 변수 Q를 이용해서 filter를 적용하면 된다.

![orm filter](./images/orm filter.png)
![post 내용 filter](./images/post 내용 filter.png)
4. 이외에도 자주 쓰일 것 같은 orm 정렬, 수정, 삭제 등을 써봤다.
![orm정렬](./images/orm정렬.png)
![orm 수정](./images/orm 수정.png)
![orm 삭제](./images/orm .png)

---
### accounts
accounts 앱에서는 user model을 일대일로 참조하는 Profile 모델과 친구 맺기 기능을 위한 Friend 모델을 만들었다.
```
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.TextField(max_length=10, unique=True)
    university = models.TextField(max_length=16)
    enter_year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2030)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nickname}'
 ```
 enter_year는 입학년도 값인데, 구간 설정을 위해 from django.core.validators import MinValueValidator, MaxValueValidator를 이용했다.
 
 
 친구 맺기 기능에서 많이 해맸다. 내가 생각한 것은 현재 나의 profile정보와 친구의 profile정보를 둘다 저장하는 Friend모델을 만드는 방법이였다.
 ```
  class Friend(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.nickname}"
 ```
 다만, 중복저장이 문제였다ㅜㅜㅜ
 if문으로 현재 나의 Friend객체에 있는 값들을 비교하고 싶은데, 두 값을 동시에 비교하는 것이 어려웠다. 게다가 둘다 Profile객체로 받아오니 굉장히 헷갈렸다....
 아직도 해결을 못했다. 방법을 알려주세요..
 ```
 def new_friend(request, profile_id):
    me = request.user.profile
    friend = get_object_or_404(Profile, pk=profile_id)
    new_friend=Friend()
    new_friend.user=me
    new_friend.friend=friend
    new_friend.save()
    return render(request, 'accounts/home.html')
 ```
 문제의 코드...참고로 profile_id값은 내가 아닌 다른 사람의 값이다.
 
 ---
 ### posts
 Post와 Comment를 구현하면서 html로부터 값을 받아오는 법을 새롭게 알게 됐다.
 그동안 html은 거의 구현하지 않았는데, 굉장히 많은 type이 있어 받아오기가 쉬웠다. 심지어 date, time도 별도로 있다! 
 그리고 checkbox를 이용해 True값이나 False값을 저장하는 법을 찾았다. 
 ```
 def create(request):
    me=request.user.profile
    if request.method == "POST":
        new_post=Post()
        new_post.content=request.POST['content']
        new_post.user = me
        if len(request.POST.getlist('is_anony')) == 0:
            new_post.is_anony = False
        else:
            new_post.is_anony = True
        if len(request.POST.getlist('is_question')) == 0:
            new_post.is_question = False
        else:
            new_post.is_question= True
        new_post.image=request.FILES['image']
        new_post.save()
        return redirect('posts:home')
    return render(request, 'posts:home')
```
에브리타임은 익명과 질문글을 선택하는 기능이있어 booleanfield를 적극 활용했다.

---
### timetables
시간표를 어떻게 구현할까 고민하다가 댓글과 비슷하게 만들기로 했다.
시간표(timetable)모델과 이를 1:N으로 참조하는 과목(subject)모델을 만들었다.
```
day:
<br>
    <input type="radio" value="Monday" name="day"> Monday
    ~~
    <input type="radio" value="Sunday" name="day"> Sunday
<br>
end_time:
<br>
    <input name="end_time" type="time">
<br>
```
 이번에는 radio type을 이용하였다. Subject모델의 week가 내가 만든 WEEK_CHOICE에서 선택하도록 만들었기 때문에, 혹시 오타로 잘못 입력하면 귀찮아져서...
 또, time type을 이용했다. 다만 이런 type들을 사용할때 request.POST에서 잘못인식하고 오류를 일으킬 수 있다. 그럴때는 reqeust.POST.get('~')으로 받아온다.
 
 ---
 ### ERDCloud
 ![erd](./images/erd.png)

 ---
 ### 자잘한 오류들 및 참고
 - database를 건드리다가 돌이킬수없는 실수를 했다...
 drop database 'DB명' 으로 database 삭제 후 다시 migrate 해줌.
 - 가상환경에서 django가 제대로 설치됐는지 확인하기
 django가 써져 있어 설치된 줄 알았는데 아니였다. package 두 번 클릭하니 설치가 됐다..
 - 환경변수 설치하는 라이브러리는 ~~environ~~django-environ
 - html 건드리면서 참고한 사이트
 [html type 정리] (http://www.tcpschool.com/html-input-types/number)
 
 ---
 ### 회고...느낀점...
 어렵다...그치만 재밌다...shell도 새로 써봐서 이것저것 만져보고, 주어진 기능을 어떻게 구현할 지 계속 고민하였다. 조금 이상하게 구현된 것도 있지만...다른 사람들은 어떻게 해결했을지도 궁금하다. 
 
 시간이 조금 부족했던 점이 아쉽다. html도 좀 멋있게..에브리타임처럼 만들고 싶었는데 기능 구현하기만해도 바빠서 그냥 알아볼 수 있을 정도만 구현했다ㅜ
 
 django에서는 form 기능을 제공해서 내가 모델을 수정해도 다른 함수들을 편하게 구현할 수 있다. 하지만 form으로 하면 html이 좀..안예쁘다...그리고 자잘한 기능들을 계속확인하려고 일부러 form 활용을 안했는데...form을 사용하면서 view를 자유롭게 다루는 것이 가능한가?? 아직 그것까지는..배운게없어서 모르겠다.

 
 
 
