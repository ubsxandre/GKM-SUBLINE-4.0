function alertSuccess(message) {
  Swal.fire({
    title: 'Good job!',
    text: message,
    icon: 'success',
    showConfirmButton: false,
    timer: 1500,  
    customClass: {
      confirmButton: 'btn btn-primary waves-effect waves-light'
    },
    buttonsStyling: false
  });
};

function alertError(message) {
  Swal.fire({
    icon: 'error',
    title: 'Oops...',
    // timer: 2000,         
    text: message,
    customClass: {
      confirmButton: 'btn btn-primary waves-effect waves-light'
    },
    buttonsStyling: false
  });
};

function alertConfirmSave(message, onConfirm) {
  Swal.fire({
    title: 'Are you sure?',
    text: message || "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: "Yes, I'm Sure!",
    customClass: {
      confirmButton: 'btn btn-primary me-3 waves-effect waves-light',
      cancelButton: 'btn btn-outline-secondary waves-effect'
    },
    buttonsStyling: false
  }).then(function (result) {
    if (result.isConfirmed && typeof onConfirm === 'function') {
      onConfirm();
    }
  });
}


const alertModal = {success: alertSuccess, error: alertError, confirmSave: alertConfirmSave};


// Function For Toolltip in Datatable
function initializeTooltips() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

