from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_registration.forms import User
from G4Marketplace import settings
from item.models import Category, Item
from .forms import SignupForm
from .models import Contact
from .tokens import account_activation_token
from verify_email.email_handler import send_verification_email
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages


def index(request):
    items = Item.objects.filter(is_sold=False)
    user_color = request.session.get('user_color', None)
    categories = Category.objects.all()
    items_per_page = 12
    paginator = Paginator(items, items_per_page)
    # Get the page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Attempt to convert the page parameter to an integer
        page = int(page)
        if page < 1:
            # If the page is negative or zero, redirect sa first page
            items = paginator.get_page(1)
        else:
            # Get the Page object for the requested page
            items = paginator.get_page(page)
    except (ValueError, TypeError):
        # Handle non-integer or missing page parameter by showing the first page
        items = paginator.get_page(1)
    except EmptyPage:
        # If the page is out of range, for example 1000, REDIRECT LAST PAGE
        items = paginator.get_page(paginator.num_pages)  # LAST PAGE NA AVAIL

    context = {
        'items': items,
        'categories': categories,
        'user_color': user_color if user_color else 'primary'
    }
    return render(request, 'core/index.html', context)


def contact(request):
    contacts = None

    if request.user.is_superuser:
        contacts = Contact.objects.all().order_by('created_at')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        comment = request.POST.get("comment")
        query = Contact(name=name, email=email, subject=subject, comment=comment)
        query.save()
        messages.success(request, 'Thanks for reaching us. We will get back to you soon.')
        return redirect('/contact')

    return render(request, 'core/contact.html', {'contacts': contacts})


def send_email(request, subject, email, name):
    subject = ('Re:' + subject)
    email = email
    name = name
    print(subject)

    if request.method == "POST":
        print("request.POST")
        message = request.POST.get("message")
        message_data = {
            'name': name,
            'email': email,
            'comment': message,
            'subject': subject,

        }
        html_message = render_to_string('core/email_template.html', message_data)
        plain_message = strip_tags(html_message)

        if subject and message and email:
            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
                return redirect('/')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            return HttpResponse('Invalid form data')
    context = {
        'subject': subject,
        'email': email,
        'name': name,
    }
    return render(request, 'dashboard/email_response.html', context)


def about(request):
    return render(request, 'core/about.html')

def signup(request):
    if request.user.is_authenticated: return redirect('index')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # Send activation email
            send_verification_email(request, form)
            return redirect('request_new_activation_link')

    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = uidb64
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('login')

    messages.error(request, 'Activation link is invalid!')
    return HttpResponse('Activation link is invalid.')


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': user.pk,
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })

    email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[user.email])

    if email.send():
        messages.success(request, 'Please confirm your email address to complete the registration')
    else:
        messages.error(request, 'Failed to send email confirmation. Please try again later.')


def request_new_activation_link(request):
    if request.user.is_authenticated: return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                send_activation_email(request, user)
                messages.success(request, 'A new activation link has been sent to your email address.')
            else:
                messages.warning(request, 'Your account is already active.')
        except User.DoesNotExist:
            messages.error(request, 'User with that email address does not exist.')

    return render(request, 'core/request_activation_link.html')


def logout(request):
    return redirect(request, 'core/login.html')


def login_required_redirect(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return function(request, *args, **kwargs)
    return wrap

