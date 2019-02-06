# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth import login,logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User, Group

from .forms import *
#headers
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

def login_view(request):
    # If user have not logged in
    if not request.user.is_authenticated:
        context = {}
        # Set value for the action attribute of the form.
        context['form_action'] = 'login'

        if request.method == 'POST':

            # AuthenticationForm used for login.
            form = LoginForm(data=request.POST)
            if form.is_valid():

                # Form is valid and username+password match.
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request,user)

                return redirect('/home')
            else:
                # If login not success, set message.
                context['form_message'] = 'Incorrect username or password.'
                context['message_type'] = 'alert-danger'
        else:
            form = LoginForm()
        context['form'] = form

        return render(request, "account/login.html", context)
    # If user have logged in.
    else:
        return redirect('/home')

def logout_view(request):
    logout(request)
    return redirect('/home')


def register_view(request):
    # If user have not logged in
    if not request.user.is_authenticated:
        context = {}
        # Set value for the action attribute of the form.
        context['form_action'] = 'register'

        if request.method == 'POST':
            form = RegisterForm(request.POST)
            # If form is valid, try create account
            if form.is_valid():

                # Add user to User DB
                user = form.save()
                #user.is_active = False

                user.save()

                # Add user to group
                group_type = form.cleaned_data.get('user_type')
                user_group = Group.objects.get(id=group_type)
                user_group.user_set.add(user)

                email = form.cleaned_data.get('email')
                #send_email(request, email,user)
                send_email_2(request, email,user)

                return redirect('/account/email-confirmation/')
            else:
                # If not success, set message.
                context['message_type'] = 'alert-danger'
        else:
            form = RegisterForm()
        context['form'] = form

        return render(request, "account/register.html", context)
    # If user have logged in.
    else:
        return redirect('/home')

from django.core import mail

def send_email_2(request, to_email, user):
    current_site = get_current_site(request)
    message = render_to_string('account/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    with mail.get_connection() as connection:
        mail.EmailMessage(
            'Email verification', message, 'melon-webstore@notexist.com', [to_email],
            connection=connection,
        ).send()


def send_email(request,to_email,user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('account/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })

    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()



def email_confirmation_view(request):
    context = {}
    view_mode = False
    if request.method == 'GET':
        get = request.GET
        if(get.__contains__('mode')):
            view_mode = get['mode']

    if (view_mode=='used'):
        context['used'] = "1"
    elif (view_mode=='expire'):
        context['expire'] = "1"
    else:
        context['new'] = "1"
    return render(request, "account/email-confirmation.html", context)


def setting_view(request):
    if request.user.is_authenticated:
        user = request.user
        context = {}
        context['form_action'] = '.'
        if request.method == 'POST':
            form = EditUserProfileForm(user,request.POST)

            if form.is_valid():
                messages.add_message(request, messages.INFO, 'Saved.')
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()
                if (form.cleaned_data.get('change_password')):
                    form.save()
                update_session_auth_hash(request, user)  # Important!
                context['form'] = EditUserProfileForm(user=user)
                return render(request, "account/setting.html", context)
            else:
                # If not success, set message.
                messages.add_message(request, messages.INFO, 'Not valid.')
                context['message_type'] = 'alert-danger'
        else:
            form = EditUserProfileForm(user=user)
        context['form'] = form

        return render(request, "account/setting.html", context)
    return render(request, "403.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'account/register_success.html')
    else:
        return HttpResponse('Activation link is invalid!')

def register_success(request):
    return render(request, 'account/register_success.html')

def social_auth(request):
    if request.user.is_authenticated:
        user = request.user
        if len(user.groups.all())==0:
            return redirect('/account/choose-group')
        else:
            return redirect('/home')

def choose_group_view(request):
    if request.user.is_authenticated:
        user = request.user
        if len(user.groups.all())==0:
            context={}
            if request.method == 'POST':
                form = ChooseGroupForm(request.POST)
                # If form is valid, add user group to the account
                if form.is_valid():
                    group_type = form.cleaned_data.get('user_type')
                    user_group = Group.objects.get(id=group_type)
                    user_group.user_set.add(user)
                    return redirect('/home')
                else:
                    # If not success, set message.
                    context['message_type'] = 'alert-danger'
            else:
                form = ChooseGroupForm()
            context['form'] = form
            return render(request, 'account/choose-group.html',context)
        else:
            return redirect('/home')
    return redirect('/account/login')
