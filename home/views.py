from django.shortcuts import render
from django.template import loader,Context
from django.http import HttpResponse

def xinxiangHome(request):
	return render(request, 'home_base.html', {'logined':False})
	
def xinxiangHomeTrend(request,parm):
	 print(parm)
	 if parm == "trend1":
		return HttpResponse(loader.get_template("trend1.html").render())
	 if parm == "trend2":
		return HttpResponse(loader.get_template("trend2.html").render())
		
# def xinxiangRegist(request):
	# t = loader.get_template("register.html")
	# return HttpResponse(t.render())
	
# def xinxiangRegisting(request):
	# if request.method == 'POST':
		# username=request.POST['username']
		# password = request.POST['password']
		# user = authenticate(username=username, password=password)
		
		
		
		

# Create your views here.
