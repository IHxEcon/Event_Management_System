// Profile page JavaScript functionality

// Event data for editing - will be populated by Django template
let eventData = {};

function setEventData(data) {
  eventData = data;
}

function editEvent(bookingId) {
  const event = eventData[bookingId];
  if (!event) return;

  document.getElementById("edit_booking_id").value = bookingId;
  document.getElementById("edit_event_name").value = event.name;
  document.getElementById("edit_event_date").value = event.date;
  document.getElementById("edit_event_time").value = event.time;
  document.getElementById("edit_event_location").value = event.location;
  document.getElementById("edit_event_description").value = event.description;

  document.getElementById("editModal").style.display = "block";
}

function deleteEvent(bookingId) {
  document.getElementById("delete_booking_id").value = bookingId;
  document.getElementById("deleteModal").style.display = "block";
}

function showReviewForm(bookingId) {
  const reviewForm = document.getElementById("reviewForm");
  reviewForm.action = `/dashboard/submit_review/${bookingId}`;
  document.getElementById("reviewModal").style.display = "block";
}

function closeModal() {
  document.getElementById("editModal").style.display = "none";
}

function closeDeleteModal() {
  document.getElementById("deleteModal").style.display = "none";
}

function closeReviewModal() {
  document.getElementById("reviewModal").style.display = "none";
  // Reset form
  document.getElementById("reviewForm").reset();
  const stars = document.querySelectorAll('.rating-input input[type="radio"]');
  stars.forEach((star) => (star.checked = false));
}

// Close modal when clicking outside
window.onclick = function (event) {
  const editModal = document.getElementById("editModal");
  const deleteModal = document.getElementById("deleteModal");
  const reviewModal = document.getElementById("reviewModal");
  if (event.target === editModal) {
    editModal.style.display = "none";
  }
  if (event.target === deleteModal) {
    deleteModal.style.display = "none";
  }
  if (event.target === reviewModal) {
    reviewModal.style.display = "none";
  }
};

// Auto-hide messages after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = "0";
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 5000);
  });
});
