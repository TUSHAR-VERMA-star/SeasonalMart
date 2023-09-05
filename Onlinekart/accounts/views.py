from ast import Is
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from Cart.views import create_cart
from Cart.models import *
# Create your views here.


def register(request):
    if(request.method == 'POST'):
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        password = request.POST['password']
        username = email.split("@")[0]
        try:
            value = Account.objects.get(email=email)
            messages.success(request, 'Email Already Exist.')
            return redirect('register')
        except ObjectDoesNotExist:
            pass
        user = Account.objects.create_user(
            first_name=fname, last_name=lname, email=email, username=username, password=password)
        user.phone_number = phonenumber
        user.save()

        # USER ACTIVATION
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account'
        message = render_to_string('account_verification_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        messages.success(
            request, 'Profile is created. check you email for activation purpose!')
        return redirect('register')
    return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=create_cart(request))
                Is_Cart_Items = CartItem.objects.filter(cart=cart).exists()
                if(Is_Cart_Items):
                    Cart_Items = CartItem.objects.filter(cart=cart)
                    for Cart_Item in Cart_Items:
                        Cart_Item.user = user
                        Cart_Item.save()
            except:
                pass
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, "login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotPassword(request):
    if(request.method == "GET"):
        return render(request, "forgotPassword.html")
    else:
        email = request.POST['email']

        if(Account.objects.filter(email=email).exists()):

            user = Account.objects.get(email=email)

            # Forgot password email
            current_site = get_current_site(request)
            mail_subject = 'Forgot Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.error(request, "Email Id exist")
            return render(request, "forgotPassword.html")
        else:
            messages.error(request, "Email Id not registered")
            return render(request, "forgotPassword.html")


def resetpassword_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return render(request, "resetpassword.html")

    else:
        messages.error(request, 'Invalid link')
        return redirect('forgotPassword')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')
    else:
        return render(request, 'accounts/resetPassword.html')
