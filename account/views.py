#coding=utf-8
from django.shortcuts import render
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from account.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import re
# Create your views here.
#定义表单模型
#注册的时候需要用户名，邮箱，手机号，密码
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=100)
    email = forms.EmailField(label='电子邮件：',help_text='（必填）',required=True, error_messages={'required':"请输入邮箱地址"})
    phone = forms.CharField(label='电话号码：', help_text='（必填）', required=True, max_length=30,min_length=11,error_messages={'required':u'电话不能为空','invalid':u'请输入正确的电话号码'})
    password = forms.CharField(label='密码：', widget=forms.PasswordInput(),min_length=6,error_messages={'required':u'邮箱不能为空','invalid':u'请输入正确的邮箱','min_length':u'密码不少于6个字符'})
    password2 = forms.CharField(label='确认密码：', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['phone', 'email']
    def clean_phone(self): #clearn_字段名称
          phone = self.cleaned_data['phone']#获取对应的字段
          pattern=re.compile(r"^((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})")#设置正则验证
          if pattern.match(phone):#如果验证失败的话就会返回none
              print phone
          else:
              msg="请输入正确的手机号或座机号！"
              #self._errors["phone"] = self.error_class([msg])#设置输入框的告警文字
              raise forms.ValidationError(msg)
          self.phone=phone
          return phone

    def pwd_validate(self,p1,p2):
        return p1==p2

#登录的时候只用手机号就可以登陆
class LoginForm(forms.Form):
    phone = forms.CharField(label='电话号码：')
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())

# Create your views here.
def register2(request):
    print("hhhhhhhhh====")
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
			
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            phone = uf.cleaned_data['phone']
            email = uf.cleaned_data['email']
            #将表单写入数据库
            print('1111======')
            user = User()
            user.username = username
            user.password = password
            user.phone = phone
            user.email = email
            user.save()
            print('save======')
            #返回注册成功页面
            return render(request, 'success.html', {'username':username})
    else:
        uf = UserForm()
        return render(request, 'register.html', {'uf':uf})
#上面信息是正确的，下面是用来增加验证提示的
def register(request):
    error=[]
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2 = uf.cleaned_data['password2']
            phone = uf.cleaned_data['phone']
            email = uf.cleaned_data['email']
            #增加验证信息
            if not User.objects.all().filter(username=username):
                if uf.pwd_validate(password, password2):
                    #将表单写入数据库
                    print('1111======')
                    user = User()
                    user.username = username
                    user.password = password
                    user.phone = phone
                    user.email = email
                    user.save()
                    print('save======')
                    #返回注册成功页面
                    return render(request, 'home_base.html', {'username':username,'logined':True})
                else:
                    error.append('请输入相同的密码')
            else:
                error.append('用户名已存在')

            return render(request, 'register.html', {'uf': uf, 'error': error})
        else:
            print("error===")
            return render(request, 'register.html', {'uf': uf, 'error': error})
    else:
        uf = UserForm()
        return render(request, 'register.html', {'uf':uf, 'error':error})


#考虑改成手机号码验证
def login_validate(request,phone,password):
    rtvalue = False
    user = User.objects.get(phone=phone,password=password)
    #user = authenticate(phone=phone,password=password)
    if user is not None:
        return True,user.username

    return rtvalue,''

def Log(request):
    error = []
    if request.method == 'POST':
		print("login_success")
        form = LoginForm(request.POST)
        if form.is_valid():
          data = form.cleaned_data
          phone = data['phone']
          password = data['password']
          result,name = login_validate(request, phone, password)
          if result:
            return render(request, 'home_base.html', {'username':name,'logined':True})
          else:
            error.append('Please input the correct password')
        else:
          error.append('Please input both username and password')
    else:
		print("login_panel")
        form = LoginForm()
    return render(request, 'login.html', {'error': error,'form': form})