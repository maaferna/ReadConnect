import os
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
import logging  # Add this import

from .forms import *
# Set up a logger
logger = logging.getLogger(__name__)

def index(request):
    context = {}
    return render(request, "index.html", context)


def books_retrieve(request):
    dataset_url = "https://raw.githubusercontent.com/dudeonthehorse/datasets/master/amazon.books.json"
    local_dataset_path = os.path.join("static", "datasets", "amazon.books.json")

    try:
        # Try to retrieve data from the URL
        response = requests.get(dataset_url)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as req_err:
        logger.error("RequestException: %s", req_err)
        try:
            with open(local_dataset_path, "r", encoding="utf-8") as local_file:
                data = json.load(local_file)
        except (FileNotFoundError, json.JSONDecodeError) as file_err:
            logger.error("FileError: %s", file_err)
            return JsonResponse({"error": "Dataset not found or could not be loaded."}, status=500)

    return render(request, "books_store/index.html", context={"data": data})

