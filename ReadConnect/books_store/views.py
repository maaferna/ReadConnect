import os
import json
import requests
import datetime
from dateutil import parser
from django.http import JsonResponse
from django.shortcuts import render
import logging  # Add this import
from .utils import *
from .forms import *
# Set up a logger
logger = logging.getLogger(__name__)


def index(request):
    context = {}
    return render(request, "index.html", context)


def books_retrieve(request):
    dataset_url = "https://raw.githubusercontent.com/dudeonthehorse/datasets/master/amazon.books.json"
    json_file_name = "amazon.books.json"
    json_file_path = os.path.join(parent_directory, "static", "datasets", json_file_name)

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

    # Now, each element in the JSON data has a 'formattedPublishedDate' key
    # containing the short month and year format of the 'publishedDate'.
    return render(request, "books_store/index.html", context={"data": data})

