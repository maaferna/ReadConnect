document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("bookModal");
    const modalContent = document.getElementById("bookDetails");

    const buttons = document.querySelectorAll(".open-modal-button");
    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const bookISBN = button.getAttribute("data-book-isbn");

            // Send an AJAX request to retrieve book details by ISBN
            fetch(`/get_book_details/${bookISBN}/`)
                .then(response => response.json())
                .then(data => {
                    // Check the actual structure of the data
                    console.log(data);

                    // Access the book data and author names based on the response structure
                    const book = data; // Adjust based on the actual structure
                    const authors = book.authors.join(', '); // Adjust based on the actual structure

                    // Update modalContent with book details
                    modalContent.innerHTML = `
                        <div class="modal-header">
                            <h2 class="modal-title">${book.fields.title}</h2>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class "modal-body">
                            <div class="row">
                                <p>${book.fields.longDescription}</p>
                            </div>
                            <div class="row">
                                <div class="col-3">
                                    <p><strong>Authors:</strong> ${authors}</p>
                                    <p><strong>Status:</strong> ${book.fields.status}</p>
                                    <p><strong>Number of Pages:</strong> ${book.fields.pageCount}</p>
                                    <p><strong>ISBN:</strong> ${book.fields.isbn}</p>
                                </div>
                                <div class="col">
                                    <img src="${book.fields.thumbnailUrl}" class="card-img" style="width: 200px; height: 200px;" alt="Imagen no disponible">
                                </div>
                            </div>
                        </div>
                    `;
                    modal.style.display = "block";
                })
                .catch(error => {
                    console.error("Error fetching book details:", error);
                });
        });
    });

    const closeButton = document.querySelector(".btn-close");
    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
    });


    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});




$(document).ready(function() {
    // Add change event listeners to filter form fields
    $('#author_name, #title, #category, #status, #start_date, #end_date, #start_page, #end_page, #sort_by, #sort_order').on('change', function() {
        updateBookList();
    });

    // Function to update the book list
    function updateBookList() {
        // Gather filter values
        var author_name = $('#author_name').val();
        var title = $('#title').val();
        var category = $('#category').val();
        var status = $('#status').val();
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        var start_page = $('#start_page').val();
        var end_page = $('#end_page').val();
        var sort_by = $('#sort_by').val();
        var sort_order = $('#sort_order').val();

        // Send an AJAX request to update the book list
        $.ajax({
            url: '/read_connect_books/',  // Replace with the actual URL
            type: 'GET',
            data: {
                'author_name': author_name,
                'title': title,
                'category': category,
                'status': status,
                'start_date': start_date,
                'end_date': end_date,
                'start_page': start_page,
                'end_page': end_page,
                'sort_by': sort_by,
                'sort_order': sort_order
            },
            success: function(data) {
                // Update the book list with the response data
                $('#book-list-container').html(data);
            }
        });
    }
});


// Handle form submission
$('#create-rating-form').submit(function(e) {
    e.preventDefault();  // Prevent the default form submission
    console.log('Form submitted'); // Add this line for testing

    // Get the new_rating and new_comment values
    var newRating = $('#rating').val();
    var newComment = $('#comment').val();
    var bookId = $('#book-id-input').val();  // Use book.id here
    console.log(bookId);
    // Get the CSRF token from cookies
    var csrfToken = getCookie('csrftoken');
    // Send an AJAX request to the create_book_rating view
    $.ajax({
        url: '/create_book_rating/' + bookId + '/',
        type: 'POST',
        data: {
            new_rating: newRating,
            new_comment: newComment,
            csrfmiddlewaretoken: csrfToken
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(response) {
            // Update the book list with applied filters
            console.log('AJAX URL:', '/create_book_rating/' + bookId + '/');
             console.log('Rating and comment submitted successfully.');
            // Reload the book list based on your filtering criteria
            updateBookList();
        },
        error: function(xhr, status, error) {
            if (xhr.status === 302) {
                // Handle the 302 status here, e.g., show a message to the user
                console.log('Redirection occurred');
            } else {
                // Handle other errors
            }
        }
    });
});




function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log('CSRF Token:', cookieValue); // Add this line for debugging
    return cookieValue;
}

 document.addEventListener('DOMContentLoaded', function () {
        // Access the filter parameters from the URL and populate the hidden fields
        var authorName = getParameterByName('author_name');
        var title = getParameterByName('title');
        // Populate other hidden fields similarly

        // Update the value of the hidden fields
        document.querySelector('input[name="author_name"]').value = authorName;
        document.querySelector('input[name="title"]').value = title;
        // Update other hidden fields similarly

        // Function to get URL query parameters by name
        function getParameterByName(name, url) {
            if (!url) url = window.location.href;
            name = name.replace(/[\[\]]/g, '\\$&');
            var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
            var results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, ' '));
        }
    });

