document.addEventListener('DOMContentLoaded', function () {
    var borrowBookModal = document.getElementById('borrowBookModal');
    borrowBookModal.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget;
      var bookTitle = button.getAttribute('data-book-title');
      var bookIsbn = button.getAttribute('data-book-isbn');
  
      var modalTitle = borrowBookModal.querySelector('.modal-title');
      var bookIsbnInput = borrowBookModal.querySelector('#bookIsbn');
      var userIdInput = borrowBookModal.querySelector('#userId');
  
      modalTitle.textContent = 'Borrow ' + bookTitle;
      bookIsbnInput.value = bookIsbn;
  
      // Pre-fill user ID if available
      userIdInput.value = "123";  // Replace with actual user ID
    });
  });