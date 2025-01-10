// Add event listeners to all edit buttons
document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", () => {
      // Get book details from data attributes
      const isbn = button.getAttribute("data-isbn");
      const titre = button.getAttribute("data-titre");
      const author = button.getAttribute("data-author");
      const category = button.getAttribute("data-category");
      const url = button.getAttribute("data-url");
      const quantite = button.getAttribute("data-quantite"); // Updated to use quantite
  
      // Pre-fill the edit modal form
      document.getElementById("editIsbn").value = isbn;
      document.getElementById("editTitre").value = titre;
      document.getElementById("editAuthor").value = author;
      document.getElementById("editCategory").value = category;
      document.getElementById("editUrl").value = url;
      document.getElementById("editQuantite").value = quantite; // Updated to use quantite
  
      // Show the edit modal
      const editModal = new bootstrap.Modal(document.getElementById("editBookModal"));
      editModal.show();
    });
  });
  
  // Handle edit form submission
  document.getElementById("editBookForm").addEventListener("submit", function (event) {
    event.preventDefault();
  
    // Get form data
    const formData = new FormData(this);
  
    // Send data to the server using Fetch API
    fetch("/modifier_livre", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url; // Redirect to the livres page
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  
    // Hide the modal after submission
    const modal = bootstrap.Modal.getInstance(document.getElementById("editBookModal"));
    modal.hide();
  });
  
  // Handle add book form submission
  document.getElementById("addBookForm").addEventListener("submit", function (event) {
    event.preventDefault();
  
    // Get form data
    const formData = new FormData(this);
  
    // Send data to the server using Fetch API
    fetch("/ajouter_livre", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url; // Redirect to the livres page
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  
    // Hide the modal after submission
    const modal = bootstrap.Modal.getInstance(document.getElementById("addBookModal"));
    modal.hide();
  
    // Optionally, reset the form
    this.reset();
  });
  
  // Variable to store the ISBN of the book to delete
  let isbnToDelete = null;
  
  // Add event listeners to all delete buttons
  document.querySelectorAll(".delete-btn").forEach((button) => {
    button.addEventListener("click", () => {
      // Get the ISBN of the book to delete
      isbnToDelete = button.getAttribute("data-isbn");
  
      // Show the delete confirmation modal
      const deleteModal = new bootstrap.Modal(document.getElementById("deleteConfirmationModal"));
      deleteModal.show();
    });
  });
  
  // Handle the confirm delete button click
  document.getElementById("confirmDeleteButton").addEventListener("click", () => {
    if (isbnToDelete) {
      // Send a DELETE request to the server
      fetch(`/supprimer_livre/${isbnToDelete}`, {
        method: "DELETE",
      })
        .then((response) => {
          if (response.redirected) {
            window.location.href = response.url; // Redirect to the livres page
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
  
      // Hide the modal after submission
      const modal = bootstrap.Modal.getInstance(document.getElementById("deleteConfirmationModal"));
      modal.hide();
    }
  });
  
  // Ensure backdrop is removed when modal is hidden
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('hidden.bs.modal', function () {
      document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.remove();
      });
    });
  });