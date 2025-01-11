document.addEventListener("DOMContentLoaded", function () {
    // Get references to the modals and buttons
    const selectBorrowerModal = new bootstrap.Modal(
      document.getElementById("selectBorrowerModal")
    );
    const returnBookModal = new bootstrap.Modal(
      document.getElementById("returnBookModal")
    );
    const borrowerSelect = document.getElementById("borrowerSelect");
    const confirmBorrowerButton = document.getElementById("confirmBorrowerButton");

    // Handle the "Confirm" button in the first modal
    confirmBorrowerButton.addEventListener("click", function () {
      // Get the selected option
      const selectedOption = borrowerSelect.selectedOptions[0];

      if (selectedOption.value) {
        // Get the borrower details from the selected option
        const transactionId = selectedOption.value;
        const userName = selectedOption.getAttribute("data-user-name");
        const dueDate = selectedOption.getAttribute("data-due-date");
        const bookTitle = selectedOption.getAttribute("data-book-title");

        // Close the first modal
        selectBorrowerModal.hide();

        // Set the selected borrower's details in the second modal
        document.getElementById("modalBookTitle").textContent = bookTitle;
        document.getElementById("modalDueDate").textContent = dueDate;

        // Calculate and display late fees (if applicable)
        const currentDate = new Date();
        const dueDateObj = new Date(dueDate);
        const delay = Math.max(0, (currentDate - dueDateObj) / (1000 * 60 * 60 * 24)); // Delay in days
        const lateFees = delay > 0 ? `MAD${(delay * 5).toFixed(2)}` : "MAD 0.00"; // Example: $0.50 per day
        document.getElementById("modalLateFees").textContent = lateFees;

        // Set the transaction ID in the hidden input field
        document.getElementById("modalTransactionId").value = transactionId;

        // Show the second modal
        returnBookModal.show();
      } else {
        alert("Please select a borrower.");
      }
    });
  });