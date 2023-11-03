from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from core.forms import SignupForm
from dashboard.forms import EditUserForm
from item.models import Item
from profile.forms import UserUpdateForm
from profile.models import Profile
from django.core.paginator import Paginator, EmptyPage



@login_required
def index_d(request):
    items = Item.objects.filter(created_by=request.user)
    users = User.objects.all()
    user_id = request.user.id
    items_per_page = 8
    users_per_page = 6
    # Create a Paginator object for items
    item_paginator = Paginator(items, items_per_page)
    # Get the page number for items from the request's GET parameters
    item_page = request.GET.get('item_page')
    try:
        # Attempt to convert the item_page parameter to an integer
        item_page = int(item_page)
        if item_page < 1:
            # If the page is negative or zero, redirect sa first page
            items = item_paginator.get_page(1)
        else:
            # Get the Page object for the requested page
            items = item_paginator.get_page(item_page)
    except (ValueError, TypeError):
        # Handle non-integer or missing item_page parameter by showing the first page
        items = item_paginator.get_page(1)
    except EmptyPage:
        # If the page is out of range, for example 1000, REDIRECT LAST PAGE
        items = item_paginator.get_page(item_paginator.num_pages)  # LAST PAGE NA AVAIL
    # Create a Paginator object for users
    user_paginator = Paginator(users, users_per_page)
    # Get the page number for users from the request's GET parameters
    user_page = request.GET.get('user_page')

    try:
        # Attempt to convert the user_page parameter to an integer
        user_page = int(user_page)
        if user_page < 1:
            # If the page is negative or zero, redirect sa first page
            users = user_paginator.get_page(1)
        else:
            # Get the Page object for the requested page
            users = user_paginator.get_page(user_page)
    except (ValueError, TypeError):
        # Handle non-integer or missing user_page parameter by showing the first page
        users = user_paginator.get_page(1)
    except EmptyPage:
        # If the page is out of range, for example 1000, REDIRECT LAST PAGE
        users = user_paginator.get_page(user_paginator.num_pages)  # LAST PAGE NA AVAIL

    return render(request, 'dashboard/index_d.html', {
        'items': items,
        'user_id': user_id,
        'users': users
    })


def add_user(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = True
                user.save()
                return redirect('dashboard:index_d')

        else:
            form = SignupForm()

        return render(request, 'core/signup.html', {'form': form})


def delete_user(request, user_id):
    if request.user.is_superuser:
        try:
            user_to_delete = User.objects.get(pk=user_id)
            user_to_delete.delete()
            return redirect('dashboard:index_d')
        except User.DoesNotExist:
            raise Http404("User does not exist")
    else:
        raise Http404("Permission denied")


def edit_user(request, user_id):
    print(user_id)
    instance = User.objects.get(pk=user_id)
    if request.user.is_superuser:
        user = get_object_or_404(Profile, user=instance)
        print(user)
        if request.method == 'POST':

            form = EditUserForm(request.POST, instance=user)
            user_form = UserUpdateForm(request.POST, instance=instance)
            if form.is_valid() and user_form.is_valid():
                user = form.save()
                user.is_active = True
                user.save()
                user_form.save()
                return redirect('dashboard:index_d')

        else:
            form = EditUserForm(instance=user)
            user_form = UserUpdateForm(instance=instance)
            context = {
                'form': form,
                'user_form': user_form,
            }
        return render(request, 'dashboard/edit_user.html', context)
    else:
        raise Http404("Permission denied")
