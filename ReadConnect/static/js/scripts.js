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
                        <div class="modal-body">
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
                            </div
                        </div>
                    `;
                    modal.style.display = "block";
                })
                .catch(error => {
                    console.error("Error fetching book details:", error);
                });
        });
    });

    const closeButton = document.querySelector(".close");
    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});





