import os
import json
import requests
from datetime import datetime
import pytz
from dateutil import parser
from django.http import JsonResponse
from django.shortcuts import render
import logging  # Add this import
from django.core import serializers
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import BookStatusForm

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
def read_connect_books(request):
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
    '''
    # Create a dictionary to hold the filter criteria
    filters = {}
    
    
    add_filter(filters, 'authors__name__icontains', author_name)
    add_filter(filters, 'title__icontains', title)
    add_filter(filters, 'categories__name__icontains', category)
    add_filter(filters, 'status', status)
    add_filter(filters, 'publishedDate', start_date, 'gte')
    add_filter(filters, 'publishedDate', end_date, 'lte')

    if start_page is not None:
        try:
            start_page = int(start_page)
            add_filter(filters, 'pageCount', start_page, 'gte')
        except ValueError:
            pass

    if end_page is not None:
        try:
            end_page = int(end_page)
            add_filter(filters, 'pageCount', end_page, 'lte')
        except ValueError:
            pass
    '''
    # Use the filter criteria to retrieve books
    # Define default values for each filter
    default_start_date = "1900-10-01T00:00:00.000-0700"
    default_end_date = "2023-10-01T00:00:00.000-0700"
    default_start_page = 0  # Set your desired default value
    default_end_page = 10000  # Set your desired default value

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
    books = Book.objects.filter(query).order_by(sort_by if sort_order == 'asc' else f"-{sort_by}")

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

    context = {'data': book_list, 'filters_values': filters_values, 'page': page,
               'userbookstatus_titles_want_to_read': userbookstatus_titles_want_to_read,
               'userbookstatus_titles_currently_reading': userbookstatus_titles_currently_reading,
               }

    return render(request, "books_store/read_connect.html", context)
