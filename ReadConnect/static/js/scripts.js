document.addEventListener("DOMContentLoaded", function() {
    const showMoreButtons = document.querySelectorAll(".show-more-btn");

    showMoreButtons.forEach((button) => {
        button.addEventListener("click", function() {
            const targetId = button.getAttribute("data-target");
            const longDescription = document.querySelector(`[data-target="${targetId}"]`);

            if (longDescription.classList.contains("d-none")) {
                longDescription.classList.remove("d-none");
                button.textContent = "Show Less";
            } else {
                longDescription.classList.add("d-none");
                button.textContent = "Show More";
            }
        });
    });
});

// JavaScript to handle opening the modal
const modal = document.getElementById("bookModal");
const modalContent = document.getElementById("bookDetails");

// Add an event listener to all the buttons with class "open-modal-button"
const buttons = document.querySelectorAll(".open-modal-button");
buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const bookId = button.getAttribute("data-book-id");

        // Send a request to retrieve book details by ID and populate modalContent
        // You will need to create a view in your Django application for this purpose
        fetch(`/get_book_details/${bookId}/`) // Replace with your actual URL
            .then(response => response.json())
            .then(data => {
                // Update modalContent with book details
                modalContent.innerHTML = `<h2>${data.title}</h2><p>${data.description}</p>`;
                modal.style.display = "block";
            })
            .catch(error => {
                console.error("Error fetching book details:", error);
            });
    });
});

// Close the modal when the close button is clicked
const closeButton = document.querySelector(".close");
closeButton.addEventListener("click", () => {
    modal.style.display = "none";
});

// Close the modal if the user clicks outside of it
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

