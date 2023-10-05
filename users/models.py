from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    """ 사용자 모델을 생성하고 관리하는 클래스입니다. """

    def create_user(self, email, password, username):
        """ 일반 사용자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')
        
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        """ 관리자를 생성하는 메서드입니다. """
        if not email:
            raise ValueError('유효하지 않은 이메일 형식입니다.')
        
        user = self.create_user(
            email,
            password=password,
            username=username,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

"""
위의 (email, password=password, username=username,)에서 각 인자 전달 방식이 달라서 정리해봤습니다.

< 함수 호출 시 인자 전달 방식 >

1. 키워드 인수 ('인자이름=값' in python)
키워드 인수는 인자를 함수에 전달할 때 인자의 이름을 함께 지정하는 방식
인자의 순서와 상관없이 명시적으로 어떤 인자에 어떤 값을 전달하는지 명확하게 지정할 수 있습니다.
(email=email, password=password,)

2. 위치 인수
위치 인수는 인자를 함수에 전달할 때 인자의 순서에 따라 전달하는 방식
함수 정의 시에 정의된 매개변수의 순서대로 값을 전달해야 합니다.
( email, password,)
"""

class User(AbstractBaseUser):
    
    """
    커스텀 사용자 모델을 정의하는 클래스입니다.
    
    - email(필수) : 로그인 시 사용할 사용자의 이메일 주소입니다.
        - 다른 사람의 이메일과 중복되지 않도록 설정합니다.
    - password(필수) : 사용자의 비밀번호입니다.
    - username(필수) : 사용자의 아이디입니다.
        - 다른 사람의 아이디와 중복되지 않도록 설정합니다.
    - profile_img : 사용자의 프로필 사진입니다.
    - birthday : 사용자의 생년월일입니다.
    - following : 사용자간 팔로우 관계입니다.
    - created_at : 회원가입 일자 및 시간입니다.
    - updated_at : 회원 정보 마지막 수정 일자 및 시간입니다.
    - is_admin : 관리자 권한 여부입니다.
        - True 혹은 False를 저장할 수 있으며, 기본값으로 True를 저장하도록 설정합니다.
    - is_active : 계정 활성화 여부입니다.
        - True 혹은 False를 저장할 수 있으며, 기본값으로 True를 저장하도록 설정합니다.
    """
    
    username = models.CharField('아이디', max_length=30, unique=True)
    password = models.CharField('비밀번호', max_length=255)
    email = models.EmailField('이메일', max_length=255, unique=True)
    profile_img = models.ImageField('프로필 이미지', upload_to='profile_images/', blank=True, null=True)
    birthday = models.DateField('생년월일', blank=True, null=True)
    following = models.ManyToManyField('self', verbose_name='팔로잉', symmetrical=False, related_name='followers', blank=True)
    created_at = models.DateField('가입일', auto_now_add=True)
    updated_at = models.DateField('수정일', auto_now=True)
    is_admin = models.BooleanField('관리자 권한 여부', default=False)
    is_active = models.BooleanField('계정 활성화 여부', default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin