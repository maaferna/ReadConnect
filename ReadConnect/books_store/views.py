import os
import json
import requests
from datetime import datetime
import pytz
from dateutil import parser

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

import logging  # Add this import
from django.core import serializers

from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.db.models import Q, Avg, Case, When, Value, IntegerField, F, Count, ExpressionWrapper, fields, DecimalField, DateTimeField, FloatField
from django.utils import timezone  # Import the timezone module

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string

from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated


from .serializers import *
from .utils import *
from .forms import *
from .models import *
from .paginations import CustomPagination

# Set up a logger
logger = logging.getLogger(__name__)



def index(request):
    context = {}
    return render(request, "index.html", context)


def books_retrieve(request):
    dataset_url = "https://raw.githubusercontent.com/dudeonthehorse/datasets/master/amazon.books.json"
    json_file_name = "amazon.books.json"
    json_file_path = os.path.join(parent_directory, "static", "datasets", json_file_name)

    filters_values = []
    try:
        # Try to retrieve data from the URL
        response = requests.get(dataset_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        logger.error("RequestException: %s", req_err)
        try:
            with open(json_file_path, "r", encoding="utf-8") as local_file:
                data = json.load(local_file)
        except (FileNotFoundError, json.JSONDecodeError) as file_err:
            logger.error("FileError: %s", file_err)
            return JsonResponse({"error": "Dataset not found or could not be loaded."}, status=500)

    unique_statuses = list(set(item.get('status', '') for item in data))
    # Get the author_name from the GET request parameters
    author_name = request.GET.get('author_name')
    title = request.GET.get('title')
    category_filter = request.GET.get('category', '')
    categories = [category.strip() for category in category_filter.split(',')]
    status = request.GET.get('status')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    # Get the start_page and end_page from the GET request parameters
    start_page = request.GET.get('start_page')
    end_page = request.GET.get('end_page')

    # Parse the start_page and end_page as integers
    try:
        start_page = int(start_page)
    except (ValueError, TypeError):
        start_page = None

    try:
        end_page = int(end_page)
    except (ValueError, TypeError):
        end_page = None

    # Filter data based on the author_name
    if author_name:
        data = [item for item in data if author_name.lower() in " ".join(item.get('authors', [])).lower()]
        filters_values.append(author_name)
    else:
        filters_values.append('')

    if title:
        data = [item for item in data if title.lower() in item.get('title', '').lower()]
        filters_values.append(title)
    else:
        filters_values.append('')

    if categories:
        data = [item for item in data if
                any(category.lower() in " ".join(item.get("categories", [])).lower() for category in categories)]
        filters_values.append(category_filter)
    else:
        filters_values.append('')

    if status:
        data = [item for item in data if status.lower() in item.get('status', '').lower()]
        filters_values.append(status)
    else:
        filters_values.append('')

    # Parse the start and end dates from the form input fields
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        start_date = pytz.timezone('UTC').localize(start_date)  # Add a time zone
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        end_date = pytz.timezone('UTC').localize(end_date)  # Add a time zone
    else:
        end_date = None

    # Filter data based on the parsed start and end dates
    filtered_data = []
    if start_date is not None and end_date is not None:
        for item in data:
            if 'publishedDate' in item:
                date_string = item['publishedDate']['$date']
                date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')

                if start_date and end_date:
                    if start_date <= date <= end_date:
                        filtered_data.append(item)
                elif start_date and date >= start_date:
                    filtered_data.append(item)
                elif end_date and date <= end_date:
                    filtered_data.append(item)
        data = filtered_data
    elif start_date is not None:
        for item in data:
            if 'publishedDate' in item:
                date_string = item['publishedDate']['$date']
                date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')

                if start_date <= date:
                    filtered_data.append(item)
        data = filtered_data
    elif end_date is not None:
        for item in data:
            if 'publishedDate' in item:
                date_string = item['publishedDate']['$date']
                date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')

                if date <= end_date:
                    filtered_data.append(item)
        data = filtered_data

    filters_values.append(start_date)
    filters_values.append(end_date)
    filtered_data_by_page = []
    if start_page is not None and end_page is not None:
        for item in data:
            if 'pageCount' in item:
                page_count = item['pageCount']
                if (start_page is None or page_count >= start_page) and (end_page is None or page_count <= end_page):
                    filtered_data_by_page.append(item)
        data = filtered_data_by_page
    elif start_page is not None:
        for item in data:
            if 'pageCount' in item:
                page_count = item['pageCount']
                if (start_page is None or page_count >= start_page) and (end_page is None):
                    filtered_data_by_page.append(item)
        data = filtered_data_by_page
    elif end_page is not None:
        for item in data:
            if 'pageCount' in item:
                page_count = item['pageCount']
                if (start_page is None) and (end_page is not None and page_count < end_page):
                    filtered_data_by_page.append(item)
        data = filtered_data_by_page

    filters_values.append(start_page)
    filters_values.append(end_page)

    # Iterate through the JSON data and update the publishedDate
    for item in data:
        if 'publishedDate' in item:
            try:
                date_string = item['publishedDate']['$date']
                date = parser.parse(date_string)
                formatted_date = date.strftime("%b %Y")
                item['formattedPublishedDate'] = formatted_date
            except (ValueError, KeyError):
                # Handle invalid date formats or missing data
                item['formattedPublishedDate'] = "Date Unavailable"

    # Sort by section
    sort_by = request.GET.get('sort_by')
    sort_order = request.GET.get('sort_order')
    filters_values.append(sort_by)
    filters_values.append(sort_order)

    # Sort the data based on the selected criterion
    # Create a mapping from predefined values to sorting criteria
    sorting_criteria = {
        'title_sort': 'title',
        'pageCount_sort': 'pageCount',
        'publishedDate_sort': 'publishedDate',
    }

    # Sort the data based on the selected criterion
    if sort_by in sorting_criteria:
        criterion = sorting_criteria[sort_by]

        # Function to extract the key for sorting
        def get_sort_key(item):
            if criterion == 'publishedDate':
                date_info = item.get(criterion, {})
                date_str = date_info.get('$date', '')

                if date_str:
                    # Parse the date string to a datetime object
                    try:
                        date = parser.parse(date_str)
                    except ValueError:
                        # Handle invalid date strings with a default minimum date
                        date = datetime.min.replace(tzinfo=pytz.UTC)
                else:
                    # Handle cases where 'publishedDate' is missing or invalid
                    date = datetime.min.replace(tzinfo=pytz.UTC)

                return date
            elif criterion == 'title':
                return item.get(criterion, '')
            elif criterion == 'pageCount':
                return item.get(criterion, 0)

        data.sort(key=get_sort_key)

        # Determine the sorting order (ascending or descending)
        if sort_order == 'desc':
            data.reverse()

    # Now, each element in the JSON data has a 'formattedPublishedDate' key
    # containing the short month and year format of the 'publishedDate'.
    context = {"data": data, 'filters_values': filters_values,
               'unique_statuses': unique_statuses}
    return render(request, "books_store/index.html", context)


def get_book_details(request, book_isbn):
    try:
        book = Book.objects.get(isbn=book_isbn)

        # Serialize the book object, including the related authors and categories
        data = serializers.serialize('json', [book], use_natural_primary_keys=True)

        # Convert the serialized data to a list of dictionaries
        book_data = json.loads(data)[0]

        # Add author names and category names to the book data
        book_data['authors'] = [author.name for author in book.authors.all()]
        book_data['categories'] = [category.name for category in book.categories.all()]

        return JsonResponse(book_data)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)


@login_required
@require_POST
def update_book_status(request, book_isbn):
    # Get the book instance based on the ISBN
    try:
        book = Book.objects.get(isbn=book_isbn)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    user = request.user  # Assuming you have a logged-in user

    form = BookStatusForm(request.POST)

    if form.is_valid():
        # Get or create a UserBookStatus instance for the user and book
        user_book_status, created = UserBookStatus.objects.get_or_create(
            user=user,
            book=book
        )

        # Update the book status based on the form data
        user_book_status.currently_reading = form.cleaned_data.get('currently_reading', True)
        user_book_status.want_to_read = form.cleaned_data.get('want_to_read', True)
        user_book_status.save()

        return JsonResponse({"success": "Book status updated successfully"})
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)


@login_required
def read_connect_books(request, author_name='', title='', category='', status='', start_date='', end_date='', start_page='', end_page='', sort_by='', sort_order='asc'):
    # Get the query parameters from the request
    author_name = request.GET.get('author_name')
    title = request.GET.get('title')
    category = request.GET.get('category')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_page = request.GET.get('start_page')
    end_page = request.GET.get('end_page')
    sort_by = request.GET.get('sort_by')
    sort_order = request.GET.get('sort_order')

    # Use the filter criteria to retrieve books
    # Define default values for each filter
    default_start_date = "1970-10-01T00:00:00.000-0700"
    default_end_date = "2023-10-01T00:00:00.000-0700"
    default_start_page = 300 # Set your desired default value
    default_end_page = 10000  # Set your desired default value

    # Create a dictionary with the filter values
    filters_values = {
        'author_name': author_name,
        'title': title,
        'category': category,
        'status': status,
        'start_date': start_date,
        'end_date': end_date,
        'start_page': start_page,
        'end_page': end_page,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    # Store the query parameters in the session
    request.session['filter_params'] = {
        'author_name': author_name,
        'title': title,
        'category': category,
        'status': status,
        'start_date': start_date,
        'end_date': end_date,
        'start_page': start_page,
        'end_page': end_page,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    # Initialize an empty Q object to build the query
    query = Q()
    # Check if the query parameters are empty or None, and assign defaults
    if author_name:
        query &= Q(authors__name__icontains=author_name)

    if title:
        query &= Q(title__icontains=title)

    if category:
        query &= Q(categories__name__icontains=category)

    if start_date:
        query &= Q(publishedDate__gte=start_date)
    else:
        query &= Q(publishedDate__gte=default_start_date)

    if end_date:
        query &= Q(publishedDate__lte=end_date)
    else:
        query &= Q(publishedDate__lte=default_end_date)

    if start_page is not None:
        try:
            start_page = int(start_page)
            query &= Q(pageCount__gte=start_page)
        except (ValueError, TypeError):
            pass
    else:
        query &= Q(pageCount__gte=default_start_page)

    if end_page is not None:
        try:
            end_page = int(end_page)
            query &= Q(pageCount__lte=end_page)
        except (ValueError, TypeError):
            pass
    else:
        query &= Q(pageCount__lte=default_end_page)

    # Other option to make the filters
    # books = Book.objects.filter(**filters).order_by(sort_by if sort_order == 'asc' else f"-{sort_by}")

    # Default values for sort_by and sort_order
    # Get the 'sort_by' parameter from the request, or use a default value
    sort_by = request.GET.get('sort_by', 'title')  # 'title' is the default field to sort by if not provided

    # Get the 'sort_order' parameter from the request, or use a default value
    sort_order = request.GET.get('sort_order', 'asc')  # 'asc' is the default sort order if not provided

    # Ensure 'sort_by' is a valid field for sorting
    valid_sort_fields = ['title', 'pageCount', 'publishedDate']
    if sort_by not in valid_sort_fields:
        sort_by = 'title'  # Set a default value if 'sort_by' is invalid

    # Now you can use 'sort_by' and 'sort_order' in your query
    # Use the Q object to filter books
    books = Book.objects.filter(query).order_by(sort_by if sort_order == 'asc' else f"-{sort_by}")[:100]

    # Get all UserBookStatus instances for the current user
    user = request.user
    userbookstatus_want_to_read = UserBookStatus.objects.filter(user=user, want_to_read=True)
    userbookstatus_titles_want_to_read = [status.book.title for status in userbookstatus_want_to_read]

    # Get all UserBookStatus instances for the current user marked as "Currently Reading"
    userbookstatus_currently_reading = UserBookStatus.objects.filter(user=user, currently_reading=True)
    userbookstatus_titles_currently_reading = [status.book.title for status in userbookstatus_currently_reading]

    paginator = Paginator(books, 20)
    page = request.GET.get('page')

    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    # Fetch additional information for each book
    book_info = []
    for book in books:
        reviews = BookRating.objects.filter(book=book).order_by('-timestamp')
        review_count = reviews.count()

        # Calculate the average rating
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / review_count if review_count > 0 else 0

        # Fetch comments and author names
        comments = []
        for review in reviews:
            author_name = review.user.username
            comment = review.comment
            if review.user == request.user:
                author_name = "me"  # Replace the author name with "me" for the current user
            comments.append({'author_name': author_name, 'comment': comment})

        book_info.append({
            'book': book,
            'review_count': review_count,
            'average_rating': average_rating,
            'comments': comments,
        })

    book_list_html = render_to_string('books_store/read_connect.html', {'data': book_list})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # Your AJAX-specific code here
        return HttpResponse(book_list_html)

    context = {'data': book_list, 'filters_values': filters_values, 'page': page,
               'userbookstatus_titles_want_to_read': userbookstatus_titles_want_to_read,
               'userbookstatus_titles_currently_reading': userbookstatus_titles_currently_reading,
               'book_info': book_info,
               }

    return render(request, "books_store/read_connect.html", context)


@login_required
def create_book_rating(request, book_id):
    # Extract the filter parameters from the request.GET
    filter_parameters = {
        'author_name': request.GET.get('author_name', ''),
        'title': request.GET.get('title', ''),
        'category': request.GET.get('category', ''),
        'status': request.GET.get('status', ''),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'start_page': request.GET.get('start_page', ''),
        'end_page': request.GET.get('end_page', ''),
        'sort_by': request.GET.get('sort_by', ''),
        'sort_order': request.GET.get('sort_order', ''),
    }

    # You now have the filter parameters as a dictionary
    print(filter_parameters)
    if request.method == 'POST':
        new_rating = request.POST.get('new_rating')
        new_comment = request.POST.get('new_comment')

        if not new_rating:
            return JsonResponse({'error': 'New rating is required'})

        book = get_object_or_404(Book, id=book_id)

        # Try to get an existing BookRating instance, or create a new one if it doesn't exist
        book_rating, created = BookRating.objects.get_or_create(user=request.user, book=book)

        # Update the rating and comment
        book_rating.rating = new_rating
        book_rating.comment = new_comment
        book_rating.save()

        # After processing, construct the redirect URL
    redirect_url = reverse('read_connect_books')

    # Append the filter parameters as query parameters to the URL
    for key, value in filter_parameters.items():
        if value:
            redirect_url += f'&{key}={value}'
    # Extract the filter parameters from the request.GET when provided

    # Include other filter parameters similarly

    # Extract the filter parameters from the request.GET when provided
    # Pass the filter parameters to the read_connect_books view using **filter_params
    return read_connect_books(request, **filter_parameters)



@login_required
@require_POST
def update_book_rating(request, book_id):
    try:
        book_rating = BookRating.objects.get(user=request.user, book_id=book_id)
    except BookRating.DoesNotExist:
        return JsonResponse({'error': 'Rating does not exist for this book.'}, status=400)

    new_rating = request.POST.get('new_rating')
    new_comment = request.POST.get('new_comment')

    if new_rating and new_comment:
        # Update the rating and comment
        book_rating.update_rating(new_rating, new_comment)
        return JsonResponse({'message': 'Rating and comment updated successfully.'})
    elif new_rating:
        # Update only the rating
        book_rating.rating = new_rating
        book_rating.save()
        return JsonResponse({'message': 'Rating updated successfully.'})
    elif new_comment:
        # Update only the comment
        book_rating.comment = new_comment
        book_rating.save()
        return JsonResponse({'message': 'Comment updated successfully.'})
    else:
        return JsonResponse({'error': 'No data provided for update.'}, status=400)



@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UpdateUserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            print("Form is valid")
            form.save()
            print("Form saved")
            return redirect('profile')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = UpdateUserProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'books_store/edit_profile.html', context)

@login_required
def profile(request):
    # Get the user's profile data
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Annotate each book with the average rating and rating count
    user_statuses = UserBookStatus.objects.filter(user=request.user).annotate(
        average_rating=Avg('book__bookrating__rating'),
        comment_count=Count('book__bookrating__comment'),
        review_count=Count('book__bookrating'),
    )

    # Separate books with reviews (average_rating is not null) from those without reviews
    with_reviews = user_statuses.filter(average_rating__isnull=False).order_by('-average_rating', '-book__publishedDate')
    without_reviews = user_statuses.filter(average_rating__isnull=True).order_by('-book__publishedDate')

    # Combine the ordered sets of books
    user_statuses = with_reviews | without_reviews

    # Sort user_statuses by the presence of reviews, average rating, and then by publishedDate
    user_statuses = user_statuses.annotate(has_reviews=Count('book__bookrating')).order_by(
        '-has_reviews',  # Sort first by the presence of reviews (books with reviews come first)
        '-average_rating',  # Then sort by average rating in descending order
        '-book__publishedDate'  # Finally, sort by publishedDate in descending order
    )

    want_to_read_statuses = user_statuses.filter(want_to_read=True)
    currently_reading_statuses = user_statuses.filter(currently_reading=True)
    print(currently_reading_statuses)

    context = {
        'user_profile': user_profile,
        'user_statuses': user_statuses,
        'want_to_read_statuses': want_to_read_statuses,
        'currently_reading_statuses': currently_reading_statuses,
    }

    return render(request, 'books_store/profile.html', context)


class WantToReadBooksView(APIView):
    def get(self, request):
        user = self.request.user
        want_to_read_books = UserBookStatus.objects.filter(user=user, want_to_read=True)

        # You can then serialize the UserBookStatus objects and return them in the response
        serializer = UserBookStatusSerializer(want_to_read_books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserBookStatusViewSet(viewsets.ModelViewSet):
    queryset = UserBookStatus.objects.all()
    serializer_class = UserBookStatusSerializer

    @action(detail=False, methods=['GET'])
    def currently_reading_books(self, request):
        user = self.request.user
        currently_reading_statuses = UserBookStatus.objects.filter(user=user, currently_reading=True)
        books = [status.book for status in currently_reading_statuses]
        serializer =BookWithUserStatusSerializer(books, many=True)  # Use BookSerializer to serialize books
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardData(APIView):

    def get(self, request):
        # Get the user's profile data
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Get user statuses
        user_statuses = UserBookStatus.objects.filter(user=request.user)

        profile_serializer = UserProfileSerializer(user_profile)
        status_serializer = UserBookStatusSerializer(user_statuses, many=True)

        data = {
            'user_profile': profile_serializer.data,
            'user_statuses': status_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    # If the user reaches this point, they are authenticated
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_statuses = UserBookStatus.objects.filter(user=request.user)

    profile_serializer = UserProfileSerializer(user_profile)
    status_serializer = UserBookStatusSerializer(user_statuses, many=True)

    data = {
        'user_profile': profile_serializer.data,
        'user_statuses': status_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)