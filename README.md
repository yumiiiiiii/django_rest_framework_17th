# CEOS 17기 백엔드 스터디

<<<<<<< HEAD
## Q1. 로그인 인증

- Session ID + Cookie

먼저, 쿠키는 서버와 클라이언트가 연결되면 자동으로 생성되고, 유저가 데이터를 요청하고 응답할 때 정보를 담아 보내는 그릇이라고 볼 수 있다.

쿠키에 담긴 정보를 통해 사용자를 식별할 수 있다.

다만, 쿠키가 탈취되면 쿠키에 담긴 정보가 그대로 노출되므로 쿠키만 사용해서 인증하는 경우는 거의 없다.

보안을 위해 쿠키와 함께 사용하는 것이 Session이다.

보안을 위해 인증 정보를 추가적인 저장 공간에 저장한다. 이때 사용하는 식별자를 Session ID라 함.

쿠키에 Session ID를 저장하여 요청과 응답을 한다. 이 Session ID의 비교를 통해 사용자를 인증하는, 한단계 발전한 인증 방식이다.

다만, Session ID 자체가 탈취되면 그대로 보안이 뚫린다...이를 **하이재킹**이라고 한다.

- OAuth(Open Authorization)

외부 서비스의 인증 및 권한 부여를 관리한다.

발전된 방식인 OAuth 2.0이 있다.

Token을 관리하는 서버와 OAuth를 관리하는 서버가 따로 있어 인증을 도와준다...

별도의 회원가입 없이 외부 서비스에서도 인증을 가능하게하여 개인정보 보호를 위해 사용

---
## Q2. JWT

위 방식들을 보완하기 위한 인증 방식(JSON Web Token)이다.

JSON데이터를 URL형식으로 인코딩하여 직렬화한 것으로, Header.Payload.Signature로 나누어진다.(실제로 Token을 발행하니 .을 기준으로 나뉘어져 있었다!! 그동안 쓰면서도 몰랐다...
+ Header : token의 타입, 암호화 방식
+ Payload : 토큰에 담을 정보
+ Signature : 토큰이 위변조되지 않음을 증명

HTTP 헤더에 토큰을 첨부하기만 하면 인증이 가능하고, 굉장히 강력한 인증 방식이다. 또한 Session과 다르게 별도의 저장소가 필요없다(검증만 하면 정보는 같이 있으므로)

다만, 이 Token을 탈취당하면 똑같이 정보가 유출될 가능성이 있는데, 이를 막기 위한 Access/Refresh Token이 있다.
+ Access Token : 정보를 주고받기 위한 Token. 따라서 이 Token이 탈취되면 정보가 유출될 가능성이 있다...Access Token에 유효기간을 두어서 정보가 계속해서 유출될 가능성을 막을 수 있다.
+ Refresh Token : 보안을 위한 토큰. Access Token에 유효기간을 두기도 하지만, 여기에 더하여 Refresh Token을 이용해 Access Token을 새로 발급받을 수도 있다.

LocalStorage와 Cookie중 하나에 저장해서 전달한다. 둘다 장단점이 있다고 하는데, 이중에서 나는 cookie에 저장하는 방식을 사용했다.

Cookie에 저장하면 CSRF 공격에 취약하다고 하는데, CSRF 공격을 막기 위해 프론트에서 뭐 처리를 한다고 들었는다...사실 잘 모르겠음. 반대로 localstorage는 xss 공격에 강함.

---
## Q3. JWT 로그인 구현 + ADVANCDED

0️⃣커스텀 유저 모델 사용하기

django의 유저 모델은 크게 3가지가 있다.
+ 기본 User : django의 기본 User model로, 따로 커스텀을 하지 않고 settings도 설정할 필요가 없어 편리하다.
+ 다만 권한이나 확장이 어려워서 잘 사용하지 않음. 
+ AbstractUser : django의 기본 User모델을 베이스로 확장하는 형식. django의 기본 User모델의 필드는 ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', date_joined'] 가 있다.
+ 여기에 원하는 필드를 추가하거나 기존 필드를 수정하는 등으로 사용.
+ AbstractBaseUser : 기존 user모델을 사용하지 않고 거의 모든 것을 재정의 하는 함수.
+ ceos에서는 이 방식을 추천했는데...나는 기존 user모델과 함수를 열심히 사용하고, abstractuser를 이용해서 인증이 가능하기에 AbstractUser방식을 사용했다.

가장 먼저 한 것은 기존의 user 모델 수정하기ㅜㅜ..원해 user모델을 일대일로 참조하는 profile 모델을 사용했는데 jwt사용이 어려워서 수정해주었다.

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    nickname = models.TextField(max_length=10, unique=True)
    university = models.TextField(max_length=16)
    enter_year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2030)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'
```
단 settings.py에 **AUTH_USER_MODEL='accounts.User'** 설정 필수!!

1️⃣ token발행
#### REQUEST
+ URL : http://127.0.0.1:8000/accounts/api/token/
+ Method : POST
+ Body
```json
{
	"username" : "jain53791",
	"password" : "yumi1226"
}
```
#### Response
+ success
```json
{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzkwNzg0MywiaWF0IjoxNjgzMzAzMDQzLCJqdGkiOiJjOGU3MGQzYTFlOTU0NDI5OGE5MGRhZDcwMzc2ZTk1ZCIsInVzZXJfaWQiOjF9.TaAWWStl0VV8WgPRtYXPBIg5_ui7te2OpJSIukZLIiQ",
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzA0ODQzLCJpYXQiOjE2ODMzMDMwNDMsImp0aSI6Ijg0ZDY3NDVhN2YzYTQ5OGI5ZjQ4YmUzZTA2MjYzODdmIiwidXNlcl9pZCI6MX0.JO2JIuBblXE25Arjz90bnWi7YNFyodyeYH77L_LyaNE"
}
```
+ Error
```json
{
	"detail": "지정된 자격 증명에 해당하는 활성화된 사용자를 찾을 수 없습니다"
}
```

2️⃣ token을 활용한 login 구현
#### Request
+ URL : http://127.0.0.1:8000/accounts/login/
+ Method : POST
+ Body
+ Header에 Bearer라는 이름으로(??) Access Token을 넣어준다.
```json
{
	"username" : "jain53791",
	"password" : "yumi1226"
}
```
#### Response
+ success
```json
{
	"user": {
		"id": 1,
		"username": "jain53791"
	},
	"message": "login success",
	"token": {
		"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzA2MzgyLCJpYXQiOjE2ODMzMDQ1ODIsImp0aSI6IjY5ZTE5NTA5Y2Q0NzQxZjhiZGNlMmE3MzA3NDcwMWQ1IiwidXNlcl9pZCI6MX0.91E8DBp0ONrJzZEy1d8QlB4PldNOBXbTJr3PKBti2f8",
		"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzkwOTM4MiwiaWF0IjoxNjgzMzA0NTgyLCJqdGkiOiI3NjVjMjJiNjBmNDY0NTdjOGQyZWI0NGU5YjdkZjA2MSIsInVzZXJfaWQiOjF9.wiUxZGMSWg2IHQbNX28v2KFNxC9trlfWCNFMvEFM8RU"
	}
}
```
+ error(token 유효x)
```json
{
	"detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
	"code": "token_not_valid",
	"messages": [
		{
			"token_class": "AccessToken",
			"token_type": "access",
			"message": "유효하지 않거나 만료된 토큰"
		}
	]
}
```
+ error(유저 존재x)
```json
{
	"message": "존재하지 않는 유저"
}
```
- 왜인지는 모르겠는데 login할 때 token을 요구한다...login 후에도 token을 response하긴 하는데 왜인지 모르겠다.
- login 후 나오는 token을 이용해서도 똑같이 인증은 가능하다. 

3️⃣ Logout 구현
- res.set_cookie("access", access_token, httponly=True)을 이용하여 Login할 때 token을 Cookie에 저장하는 방식을 사용했다.
- 
![cookie.png](..%2F..%2Fcookie.png)
- logout은 이전과 같이 auth.logout함수를 이용했다. set_cookie의 token값에 ''값을 저장하는 방식도 있는 것 같은데, header 결과가 비슷하길래 내버려둠.
- 근데 잘 하고 있는것같지가 않다...cookie를 저장하면 계속 token이 저장되어야 하는게 아닌가?? login 후 다른 api를 이용하면 cookie는 사라진다. 이럴거면 logout함수가 필요한지...
- 그래서 일단은 계속 header에 token을 전달하는 방식으로 했다. 이게 아니면 알려주세요ㅜㅜ

4️⃣ RefreshToken
#### Request
+ URL : http://127.0.0.1:8000/accounts/login/
+ Method : POST
+ Body
```
{
	"refresh" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzkxMTU3MSwiaWF0IjoxNjgzMzA2NzcxLCJqdGkiOiI4OTRmMzdlNWU2MDI0MTQ3YjhlOGQ3NTgwNGFlYWIxYiIsInVzZXJfaWQiOjJ9.FAHcVdYW5tY9Lwp0KGxdrLGPNkAT4UlXfsi0s6grAQU"
}
```
- 발급받은 Refresh Token을 입력해준다. login할때 받은거나 api/token/으로 받은거나 상관없다...

#### Response
+ success
```json
{
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzMzA4NTg3LCJpYXQiOjE2ODMzMDY3NzEsImp0aSI6IjQwNzZkNDNmOGQ0OTRmZDU5MzgwMmUzOGQ0ZGVkMGUwIiwidXNlcl9pZCI6Mn0.u37MusKQWgUAf1007K0N3hJNJg9RO2HWlb0OLM_DinQ"
}
```
+ error(잘못된 토큰)
```json
{
	"detail": "유효하지 않거나 만료된 토큰",
	"code": "token_not_valid"
}
```
+ error(access token을 입력한 경우)->구별하는거 신기하다..
```json
{
	"detail": "잘못된 토큰 타입",
	"code": "token_not_valid"
}
```
5️⃣ 권한 설정
- permission_classes 를 이용해서 권한을 설정할 수 있다.
- TimetableViewSet(시간표관리)의 경우, 인증된 사용자만 시간표를 보고, 작성,수정,삭제가 가능하므로 permission_classes = [IsAuthenticated,]를 설정해 주었다.
- 인증이 없는 상태(여기서는 Header에 token이 전달되지 않음)인 경우,
```json
{
	"detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
}
```
- settings에서 default 권한을 설정할 수 있다.
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES' : [
         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}
```
- PostViewSet(게시물관리)는 따로 권한 설정을 안해주었는데, 따라서 default값에 따라 인증되지 않은 사용자는 GET만 가능하다.
- 참고로 위에는 default 인증방식, 즉 JWT token을 이용한 방식으로 설정한것임.
- 여러 권한들
    + AllowAny (디폴트 전역 설정) : 인증 여부에 상관없이 허용
    + IsAuthenticated : 인증된 요청에 한해서 허용
    + IsAdminUser : is_Staff=True만 허용
    + IsAuthenticatedOrReadOnly : 비인증 요청에게는 읽기 권한만 허용 
    + DjangoModelPermissions : 인증된 요청에 한해 뷰 호출을 허용하고, 추가로 장고의 모델단위 Permissions 체크
    + DjangoModelPermissionsOrAnonReadOnly : DjangoModelPermissions과 유사하나, 비인증 요청에게는 읽기만 허용
    + DjangoObjectPermissions : 비인증 요청은 거부하고, 인증된 요청은 Object에 대한 권한 체크를 수행
- 사실 아래 3개는 안써봐서 모르겠다...


---
## Reference
- [token 참고](https://velog.io/@kjyeon1101/JWT-%EC%9D%B8%EC%A6%9D%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%9C-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EB%A1%9C%EA%B7%B8%EC%9D%B8#3-%EC%9C%A0%EC%A0%80-%EC%8B%9C%EB%A6%AC%EC%96%BC%EB%9D%BC%EC%9D%B4%EC%A0%80)
- [permissions 참고](https://velog.io/@joje/Authentication%EA%B3%BC-Permission#2-%ED%97%88%EA%B0%80%EC%99%80-%EA%B6%8C%ED%95%9C-authorizations-and-permissions)


>>>>>>> 2d9b0b226879a30ce158ec64d0922cfab30ed2ec
