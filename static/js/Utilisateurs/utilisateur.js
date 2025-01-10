// Add event listeners to all edit buttons
document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const userId = button.getAttribute("data-user-id");
      const fullname = button.getAttribute("data-fullname");
      const email = button.getAttribute("data-email");
  
      document.getElementById("editUserId").value = userId;
      document.getElementById("editFullname").value = fullname;
      document.getElementById("editEmail").value = email;
  
      const editModal = new bootstrap.Modal(document.getElementById("editUserModal"));
      editModal.show();
    });
  });
  
  // Handle edit form submission
  document.getElementById("editUserForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
  
    fetch("/modifier_utilisateur", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  
    const modal = bootstrap.Modal.getInstance(document.getElementById("editUserModal"));
    modal.hide();
  });
  
  // Handle add user form submission
  document.getElementById("addUserForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
  
    fetch("/ajouter_utilisateur", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  
    const modal = bootstrap.Modal.getInstance(document.getElementById("addUserModal"));
    modal.hide();
    this.reset();
  });
  
  // Handle delete confirmation
  let userIdToDelete = null;
  
  document.querySelectorAll(".delete-btn").forEach((button) => {
    button.addEventListener("click", () => {
      userIdToDelete = button.getAttribute("data-user-id");
      const deleteModal = new bootstrap.Modal(document.getElementById("deleteConfirmationModal"));
      deleteModal.show();
    });
  });
  
  document.getElementById("confirmDeleteButton").addEventListener("click", () => {
    if (userIdToDelete) {
      fetch(`/supprimer_utilisateur/${userIdToDelete}`, {
        method: "DELETE",
      })
        .then((response) => {
          if (response.redirected) {
            window.location.href = response.url;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
  
      const modal = bootstrap.Modal.getInstance(document.getElementById("deleteConfirmationModal"));
      modal.hide();
    }
  });