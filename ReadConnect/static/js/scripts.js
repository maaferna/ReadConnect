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

