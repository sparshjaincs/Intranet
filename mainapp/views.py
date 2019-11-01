from django.shortcuts import render, redirect, HttpResponse
import requests
from django.contrib import messages
import string
from django.core.mail import EmailMultiAlternatives
from mainapp.models import NewProvisionalEmployeeMail
from .tokens import get_secret_key, verify_secret_key
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from users.forms import SignUpForm, ProfileForm
import pandas as pd
from urllib.request import Request, urlopen
import json
from urllib.parse import urlencode
from urllib.error import HTTPError
from .forms import NewProvisionalEmployeeMailForm

# Create your views here.
def homepage(request):
    return render(request, 'mainapp/homepage.html')
def Leave(request):
    return render(request, 'mainapp/Leave.html')
def Heirarchy(request):
    return render(request, 'mainapp/Heirarchy.html')
def Payroll(request):
    return render(request, 'mainapp/Payroll.html')
def Documentation(request):
    return render(request, 'mainapp/Documentation.html')
def createmantis(request):
	context = {}
	if request.method=='POST':
		data=request.POST.dict()
		username=data.get("username")
		password=data.get("password")
		email=data.get("email")
		name=data.get("name")
		access_level=data.get("opt")
		enable=data.get("enable")
		protected=data.get("protected")
		url="http://mantis.atg.party/api/rest/users/"
		header={
		'Authorization':'mhVBa0ZRB7CCOdd2AGF2RuULv8LCKSp8',
		'Content-Type':'application/json'
		}

		try:
			payload=f"{{\n  \"username\":\"{username}\",\n \"password\":\"{password}\",\n \"real_name\":\"{name}\",\n \"email\":\"{email}\",\n \"access_level\":{{\"name\":\"{access_level}\"}},\n  \"enabled\": {enable},\n \"protected\":{protected}}}"
			x=requests.post(url,headers=header,data=payload,timeout=100000)
			msg=x.json()
			context['msg'] = msg
		except Exception as exp:
		    context['msg'] = exp
	return render(request, 'mainapp/createmantis.html',context)

def Track(request):
	context = {}
	if(request.method=='POST'):
		API_KEY = request.POST.get('API')
		url="http://mantis.atg.party"
		req_url = url + "/api/rest/issues?filter_id=reported"
		header = {
		    'Authorization': API_KEY,
		    'Content-Type':'application/json'
		}
		df = pd.DataFrame(columns=['id', 'project', 'reporter', 'handler', 'summary', 'status', 'assigned_on'])
		req = Request(req_url, headers=header)
		try:
			json_resp = urlopen(req).read().decode()
			issues = json.loads(json_resp)['issues']
			for issue in issues:
			    df = df.append({
			                'id' : issue.get('id'),
			                'reporter' : issue.get('reporter').get('real_name'),
			                'project' : issue.get('project').get('name'),
			                'handler' : issue.get('handler', {}).get('real_name'),
			                'summary' : issue.get('summary'),
			                'status' :  issue.get('status').get('name'),
			                'assigned_on' : issue.get('created_at')
			                }, ignore_index=True)
			html = df.to_html(classes=["table-bordered", "table-striped", "table-hover"]).replace('\n','')
			context['html'] = html
		except HTTPError as err:
			messages.error(request, err)
	return render(request, 'mainapp/Track.html', context)

def Delete(request):
	context = {}
	if request.POST:
		data=request.POST.dict()
		user_id=data.get("User_ID")
		url = f'http://mantis.atg.party/api/rest/users/{user_id}'
		headers = {
		  'Authorization': 'mhVBa0ZRB7CCOdd2AGF2RuULv8LCKSp8'
		}
		try:
		    response = requests.request('DELETE', url, headers = headers,timeout=20000)
		    context['msg'] = response.json()
		except Exception as exp:
		    context['msg'] = "Successfully Deleted"
	return render(request, 'mainapp/delete.html',context)

def Bug(request):
	context = {}
	if request.POST:
		data=request.POST.dict()
		bug_id=data.get("Bug_ID")
		url=f'http://mantis.atg.party/api/rest/issues/{bug_id}'
		headers={
		'Authorization': 'mhVBa0ZRB7CCOdd2AGF2RuULv8LCKSp8'
		}
		try:
			response = requests.request('GET', url, headers = headers, timeout=20000)
			msg=response.json()
			context['msg'] = msg
		except Exception as exp:
			context['msg'] = exp

	return render(request, 'mainapp/bug.html',context)


@login_required()
def sendoffer(request):
	context = {}
	new_emp_form = NewProvisionalEmployeeMailForm(request.POST or None, request.FILES or None)
	context['form'] = new_emp_form
	hostname = request.get_host() + "/dummyoffer"
	if request.method=='POST':
		if(new_emp_form.is_valid()):
			email = request.POST.get('email')
			username = request.POST.get('username')
			name = request.POST.get('name')
			position_name = request.POST.get('position_name')
			pay_type = request.POST.get('pay_type')
			emp_type = request.POST.get('emp_type')
			new_user_obj = {'email' : email, 'username' : username, 'position_name' : position_name, 'name' : name, 'pay_type' : pay_type, 'emp_type' : emp_type}

			context['success_message'] = "Mail has been sent!!!"
			token = get_secret_key(new_user_obj)
			msg=EmailMultiAlternatives('ATG',"Hello\n we are from atg.dev.party\n Click on this link to get offer","jecrccanteen@gmail.com",[email])
			message = "http://" + hostname + "/" + token
			msg.attach_alternative(message,"text/html")
			msg.send()
			new_emp = new_emp_form.save(commit=False)
			new_emp.token = token
			new_emp.offer_sent_by = request.user.username
			new_emp.save()
	return render(request, 'mainapp/offer.html',context)

def dummy(request, token):
	context = {}
	token_obj = verify_secret_key(token)
	email = token_obj.get('email')
	username = token_obj.get('username')
	position_name = token_obj.get('position_name')
	name = token_obj.get('name')
	pay_type = token_obj.get('pay_type')
	emp_type = token_obj.get('emp_type')
	request.session['email'] = email
	request.session['username'] = username
	request.session['name'] = name
	request.session['position_name'] = position_name
	request.session['pay_type'] = pay_type
	request.session['emp_type'] = emp_type

	if NewProvisionalEmployeeMail.objects.filter(email=email, token=token).exists():
		context['user'] = username
		return render(request,'mainapp/dummy.html',context)
	else:
		msg="Your offer is expired!!!!"
		context['msg'] = msg
	return render(request,'mainapp/greeting.html', context)


def nda(request):
	context = {}
	if request.method=='POST' and request.session['email']:
		email = request.session['email']
		username = request.session['username']
		position_name = request.session['position_name']
		name = request.session['name']
		pay_type = request.session['pay_type']
		emp_type = request.session['emp_type']
		if request.POST['submit'] == 'I Agree dummy':
			context['user'] = username
			return render(request,'mainapp/nda.html',context)

		if request.POST['submit'] == 'I Agree NDA':

			context['u_form'] = SignUpForm(initial={"email": email, "username":username, "first_name" : name}) # fill it with user details
			context['p_form'] = ProfileForm(initial={"pay_type" : pay_type, "emp_type" : emp_type})
			return render(request, 'users/createAccount.html', context)
	msg="Your offer is expired!!!!"
	context['msg'] = msg
	return render(request,'mainapp/greeting.html',context)
