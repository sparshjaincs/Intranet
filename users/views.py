from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# Create your views here.
# Restrict access to password_reset form if the user is already logged in
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from users.forms import SignUpForm, ProfileForm
from .models import Profile
import random
import requests
from django.core.mail import EmailMultiAlternatives

class MyPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'users/password_reset.html'

    # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.is_anonymous
    def test_func(self):
        return self.request.user.is_anonymous

def create(request):
    context = {}
    if(request.method == 'POST'):
        u_form = SignUpForm(request.POST) # fill it with user details
        p_form = ProfileForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            email = user.email
            username = user.username
            first_name = user.first_name
            password = username+str(random.randint(1000, 9999))
            Profile.objects.filter(user=user).delete()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'Account Created')

            '''
            creating mantis, slack account
            '''
            try:
                print("slack start", user.email)
                slack = requests.post(f"https://slack.com/api/users.admin.invite?token=xoxp-788210951796-790883779558-790885554118-6f267c84c9b3c9a5b90e2e74986c7be9&email={email}&channel='test'")
                print("slack end")
                url="http://mantis.atg.party/api/rest/users/"
                header={
                    'Authorization':'mhVBa0ZRB7CCOdd2AGF2RuULv8LCKSp8',
                    'Content-Type':'application/json'
                }
                payload = f"{{\n  \"username\":\"{username}\",\n \"password\":\"{password}\",\n \"real_name\":\"{first_name}\",\n \"email\":\"{email}\",\n  \"enabled\": true,\n \"protected\":false}}"
                mantis_resp = requests.post(url,headers=header,data=payload,timeout=100000)
                mantis = mantis_resp.json()
                mantis_confirm_mail = EmailMultiAlternatives('ATG',f"Mantis Account has been created!!\nUsername :{username}\nPassword :{password}","masterhimanshupoddar@gmail.com",[email])
                mantis_confirm_mail.send()

                messages.success(request, "Registration Successfull\nYour Intranet and Mantis Account has been created. Please check the mail for slack and mantis credentials")

            except Exception as exp:
                messages.error(request, "The credentials such as username or email may already be used in Mantis")
            return render(request, 'mainapp/homepage.html', context)
        else:
            return HttpResponse("Form was Invalid")
    return HttpResponse("You don't have the permission to access this page")
