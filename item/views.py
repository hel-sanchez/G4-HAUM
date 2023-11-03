from django.contrib.auth.decorators import login_required
from django.db.models import Q, ExpressionWrapper, F, Count, fields
from django.db.models.functions import Now
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from item.forms import NewItemForm, EditItemForm, CategoryForm, addCategory, addLocation, LocationForm
from item.models import Item, Category, PriceRange
from profile.models import Location
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages


def items(request):
    if not request.user.is_authenticated:
        return redirect('login')
        # print('asd')
    query = request.GET.get('query', '')
    category_ids = request.GET.getlist('categories')  # Get a list of selected category IDs
    location_ids = request.GET.getlist('locations')  # Get a list of selected location IDs
    price_range_ids = request.GET.getlist('price_ranges')  # Get a list of selected price range IDs
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', float('inf'))

    category = Category.objects.all()
    locations = Location.objects.all()
    items = Item.objects.filter(is_sold=False)
    price_ranges = PriceRange.objects.all()

    upvoted = request.GET.get('upvoted', False)

    # Annotate the items with upvote and downvote counts
    items = items.annotate(
        upvotes_count=Count('created_by__profile__uservote', filter=Q(created_by__profile__uservote__is_upvote=True)),
        downvotes_count=Count('created_by__profile__uservote', filter=Q(created_by__profile__uservote__is_upvote=False))
    )

    # Calculate the age of the item
    items = items.annotate(age=ExpressionWrapper(Now() - F('created_at'), output_field=fields.DurationField()))

    # To implement "Most Upvoted" sorting with recency:
    if upvoted:
        items = items.order_by('-upvotes_count', 'age')
    else:
        items = items.order_by('-upvotes_count')  # Default to sorting by most upvoted items

    print(category_ids, location_ids)
    for category_id in category_ids:
        test = category.filter(id=category_id)
        print(test)

    if category_ids:
        items = items.filter(category_id__in=category_ids)

    location_objs = []
    for location_id in location_ids:
        test2 = locations.filter(id=location_id)
        location_objs.extend(test2)

    if location_objs:
        items = items.filter(created_by__profile__location__in=location_objs)


    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Ensure that 'min_value' and 'max_value' are not empty and convert them to floats
    min_value = request.GET.get('min_value')
    max_value = request.GET.get('max_value')

    if min_value and not max_value:
        messages.error(request, "Please provide a value for 'Max Price'.")
    elif max_value and not min_value:
        messages.error(request, "Please provide a value for 'Min Price'.")
    elif min_value and max_value:
        min_value = float(min_value)
        max_value = float(max_value)

        if min_value == max_value:
            messages.error(request, "Invalid price range.")
        elif min_value < 0 or max_value < 0:
            messages.error(request, "Prices cannot be negative.")
        elif max_value - min_value > 99999:
            messages.error(request, "Price range cannot exceed 5 digits.")
        elif min_value > max_value:
            messages.error(request, 'Minimum must be lower than maximum')
        else:
            items = items.filter(price__gte=min_value, price__lte=max_value)

    else:
        return render(request, 'item/items.html', {
            'items': items,
            'query': query,
            'category': category,
            'location': locations,
            'price_ranges': price_ranges,
            'selected_price_ranges': price_range_ids,
            'min_price': min_price,
            'max_price': max_price,
            'test': category_ids,
            'test2': location_ids,
        })


    items_per_page = 24

    # Create a Paginator object
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
        items = paginator.get_page(paginator.num_pages)
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'category': category,
        'location': locations,
        'price_ranges': price_ranges,
        'selected_price_ranges': price_range_ids,
        'min_price': min_price,
        'max_price': max_price,
        'test': category_ids,
        'test2': location_ids,
    })

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=item.pk)[0:3]
    context = {
        'item': item,
        'related_items': related_items
    }
    return render(request, 'item/detail.html', context)


@login_required
def NewItem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.pk)

    else:
        form = NewItemForm()

    return render(request, 'item/new_item.html', {
        'form': form,
        'title': 'New Item'
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Check if the user is the owner or a superuser before deleting
    if request.user == item.created_by:
        item.delete()
        return redirect('dashboard:index_d')

    if request.user.is_authenticated:
        item.delete()
        return redirect('item:items')


def EditItem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.created_by or request.user.is_superuser:

        if request.method == 'POST':
            form = EditItemForm(request.POST, request.FILES, instance=item)

            if form.is_valid():
                form.save()
                return redirect('item:detail', pk=item.pk)

        else:
            form = EditItemForm(instance=item)

        return render(request, 'item/new_item.html', {
            'form': form,
            'title': 'Edit Item'
        })


def add_categories(request):
    if request.method == 'POST':
        form = addCategory(request.POST, request.FILES)  # Use 'form' instead of 'forms'

        if form.is_valid():
            category = form.save(commit=False)
            category.save()

            return redirect('item:items')

    else:
        form = addCategory()  # Initialize 'form' for GET requests

    return render(request, 'item/add_category.html', {
        'form': form,
    })


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'item/edit_category.html'
    success_url = reverse_lazy('item:items')


def deleteCategory(request, cat_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=cat_id)
        category.delete()
        return HttpResponseRedirect(reverse_lazy('item:items'))


def add_location(request):
    if request.method == 'POST':
        form = addLocation(request.POST, request.FILES)  # Use 'form' instead of 'forms'

        if form.is_valid():
            location = form.save(commit=False)
            location.save()

            return redirect('item:items')

    else:
        form = addLocation()  # Initialize 'form' for GET requests

    return render(request, 'item/add_location.html', {
        'form': form,
    })


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'item/edit_location.html'
    success_url = reverse_lazy('item:items')


def deleteLocation(request, loc_id):
    if request.user.is_superuser:
        location = get_object_or_404(Location, pk=loc_id)
        location.delete()
        return HttpResponseRedirect(reverse_lazy('item:items'))
