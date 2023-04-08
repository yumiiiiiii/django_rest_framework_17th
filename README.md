# CEOS 17기 백엔드 스터디

## CBV로 API 만들기


0️⃣ serializrs.py
```
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model=Comment
        fields=['id','user','post','content','is_anony','created_at','updated_at','reply']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    comment = CommentSerializer(many=True, source='comments', read_only=True) #source=model의 related_name 명시해야 보임

    class Meta:
        model = Post
        fields = ['id', 'user','content','is_anony','is_question','image','created_at', 'updated_at','comment']
 ```
 - user는 현재 로그인한 값을 받아와야 하므로 함수에서 따로 작성해주고, serializer에서는 ReadOnlyField를 이용해서 정의했다. 
 - source = user.nickname으로 표현하여서 nickname이 보인다.
 - comment라는 외부키를 가져오기 위해 CommentSerializer를 먼저 만들고, PostSerializer에서 comment라는 이름으로 참조했다.
 - 1:N 이므로 many=True, post에서는 건드려서는 안되므로 read_only=True 조건을 걸었다.
 - Post 데이터를 불러올 때 comment가 안보여서 찾아보니, source="related_name"을 작성해주어야 보인다. model하고 관련이 있어서 그런가...
 
 
1️⃣ 모든 데이터를 가져오는 API 만들기
```
# views.py
class PostList(APIView):
    def get(self, request, format=None):
        post=Post.objects.all()
        serializer=PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# urls.py
  path('comment/<int:comment_id>/', CommentDetail.as_view()),
  
# 결과
[
    {
        "id": 2,
        "user": "yumi3",
        "content": "수정",
        "is_anony": true,
        "is_question": false,
        "image": null,
        "created_at": "2023-04-01T22:05:45.604023+09:00",
        "updated_at": "2023-04-07T16:13:53.083834+09:00",
        "comment": [
            {
                "id": 1,
                "user": "yumi",
                "post": 2,
                "content": "sad",
                "is_anony": true,
                "created_at": "2023-04-03T20:03:55.204582+09:00",
                "updated_at": "2023-04-03T20:03:55.204582+09:00",
                "reply": null
            },
            {
                "id": 2,
                "user": "yumi",
                "post": 2,
                "content": "asd",
                "is_anony": true,
                "created_at": "2023-04-03T20:04:04.532118+09:00",
                "updated_at": "2023-04-03T20:04:04.532118+09:00",
                "reply": 1
            }
        ]
    },
    {
        "id": 5,
        "user": "yumi",
        "content": "112",
        "is_anony": true,
        "is_question": false,
        "image": null,
        "created_at": "2023-04-07T16:42:31.082424+09:00",
        "updated_at": "2023-04-07T16:47:41.146153+09:00",
        "comment": []
    }
]
```
- post객체를 전부 가져오고, PostSerializer를 이용해 JSon형식으로 변환한 후 return한다.
- PostList CBV 함수에서는 pk값이 필요없는 기능들을 구현하였다.
- serializer는 유효성 검사를 지원해주어 is_valid()함수를 이용하였고, status를 import 하여 적절한 상태코드를 반환할 수 있도록 했다.
- 특히 save()함수는 user값에 현재 로그인한 유저의 profile정보가 들어가도록 재정의하였다.


2️⃣, 3️⃣, 4️⃣ 특정 데이터 관련 API
```
# views.py
class PostDetail(APIView):

    def get_object(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, post_id, format=None):
        post=self.get_object(post_id)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id, format=None):
        post = self.get_object(post_id)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# urls.py 
  path('<int:post_id>/', PostDetail.as_view()),
  
  
# 결과 
{
    "id": 2,
    "user": "yumi3",
    "content": "수정",
    "is_anony": true,
    "is_question": false,
    "image": null,
    "created_at": "2023-04-01T22:05:45.604023+09:00",
    "updated_at": "2023-04-07T16:13:53.083834+09:00",
    "comment": [
        {
            "id": 1,
            "user": "yumi",
            "post": 2,
            "content": "sad",
            "is_anony": true,
            "created_at": "2023-04-03T20:03:55.204582+09:00",
            "updated_at": "2023-04-03T20:03:55.204582+09:00",
            "reply": null
        },
        {
            "id": 2,
            "user": "yumi",
            "post": 2,
            "content": "asd",
            "is_anony": true,
            "created_at": "2023-04-03T20:04:04.532118+09:00",
            "updated_at": "2023-04-03T20:04:04.532118+09:00",
            "reply": 1
        }
    ]
}
```

- get_object 함수를 class 내에 정의하여 pk값을 받으면 해당하는 객체를 반환하고, 없으면 404 error를 반환한다.
- GET, PUT, DELETE 모두 정상적으로 작동한다.
- 실제로 PUT이 정상적으로 실행되면 201 상태코드와 수정한 serializer.data를 return한다.
[44]

----

### CBV함수를 구현할 때, user와 관련해서 많은 오류를 겪었다.
- 처음 내가 생각한 기능은, profile을 생성하는 동시에 username과 password도 전달하여 django의 기본모델인 user가 one-to-one으로 바로 생성되게 하는 것이였다.
- 그러나 그 기능을 구현하기 어려워, user와 profile을 따로 생성하기로 했다.
- 여기서 문제점은, profile에서 참조하는 user를 찾는 것이였다. 따로 생성하다보니 profile이 참조하는 user를 찾는 것이 어려웠다.
- 구글링을 해보니, models.py에서 user가 created요청이 들어오면 해당 user를 참조하는 profile을 만드는 함수를 정의할 수 있었다.
- 이 방식으로 profile을 동시에 만들어 주었다. 다만, 처음 만들어질때는 profile의 data가 없으므로 모델 필드에 blank=True, null=True 설정을 해주었다.
- 따라서 profile은 POST와 DELETE기능을 따로 만들지 않았다.
- on_delete=models.CASCADE이므로 user가 삭제되면 profile이 삭제된다.
- profile은 user가 만들어질 때 함께 만들어진 profile의 id값으로 특정 데이터를 가져와 PUT 메소드가 가능하다.
- 또, username과 nickname은 중복이 안되도록 만들었는데 이 부분은 serializer에서도 구현을 해주었다. 같은 기능도 model, serializer, view 등 어디서 구현할지 고민하고 여러 방식으로 시도해보는 것도 좋은 것 같다.
[55]

```
# models.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save(
```

---

## Viewset으로 코드 리팩토링하기
```
# views.py
class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user.profile)
        
# urls.py
app_name = 'posts'
router = DefaultRouter()

router.register('post', PostViewSet) #comment list볼러면 설정해줘야함..
router.register('comment',CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- 코드가 완전 간단하게 줄어든다!
- perform_create로 serializer의 save 메소드를 재정의할 수 있다. user에 따로 저장하기 위해 재정의했음.
- 처음에는 PostViewSet을 불러올 때 ''로 url을 설정하지 않았는데, 그러면 CommentViewSet을 불러올 때 url을 알아보지 못한다.
- 추가로 viewset을 쓰고 싶다면 url은 등록해주는 것이 좋다.

---

## user 관련 기능
- user와 관련된 기능은 viewset으로 한번에 하기에는 확장이 어려워 CBV 방식으로 그대로 구현하였다.
- 또한 login, logout 기능을 구현했다. django 에서 기본으로 제공하는 auth 함수를 이용하였다.
- Response에 serializer.data를 그냥 넣으면 입력하는 칸에도 data를 return해서 불편함이 있다. 그럴때에는 {'data':serializer.data} 이런 식으로 하면 json형식으로 결과창에 return 한다.
- user 기능을 확장해서 token을 발행해 관리하거나, 권한 관리도 가능할 것이다. 시간이 나면 여기에 도전해야지...


---

## filter 기능
- 하나 이상의 메소드를 이용하라는 게 어떤 말인지 모르겠다...
- pip install django-filter 설치 후 post에서 filter 기능이 잘 되는 것은 확인했다.
- 만약 filter하고 싶은 내용에 외부키가 존재한다면, search_fileds=['외부키__필드이름'] 이런식으로 설정해야 오류가 안난다.
- 

---
회고 및 오류 정리
- 아무 생각 없이 github의 README를 건드렸는데, commit 후 push를 하려니 충돌이 났다. git pull로 내 branch와 같게 한 후 push 할 수 있었다...깃은 항상 어렵다.
- reply 기능은 스스로를 참조하는 외부키로 만드는 방법을 고려했는데, view를 만드는데 오류가 많이 나고 헷갈렸다...아예 다른 모델로 빼는 것도 생각을 해봐야겠다.
- 늘 유저 기능이 어렵다. 그나마 django는 유저관련 함수도 제공하고, one-to-one으로 profile을 만들 수 있어 좀 덜 헷갈리는 듯...
- 좋아요, 대댓글, 과목 등 다양한 기능의 추가 및 수정의 필요성을 느꼈다...
