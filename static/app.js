
function toggleCheckbox(selectedCheckbox) {
  const checkboxes = document.getElementsByName('userType');
  checkboxes.forEach(checkbox => {
    if (checkbox.id !== selectedCheckbox) {
      checkbox.checked = false;
    }
  });
}

//  Firebase register functions

function checkPasswordStrength(password) {
    // At least one lower case letter, one upper case letter, one digit, one special character, and at least 8 characters long
    var re = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    return re.test(password);
}

function validateForm() {
    var password = document.getElementById('password').value;
    if (!checkPasswordStrength(password)) {
        alert('Password must be at least 8 characters long, contain a lowercase letter, uppercase letter, a digit and a special character.');
        return false;
    }
    return true;
}
function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.tagSelect');

    buttons.forEach(button => {
        // Initialize Choices.js on each button
        const tagSelect = new Choices(button, {
            removeItemButton: true,
            placeholder: true,
            placeholderValue: '+ Add Tags',
            maxItemCount: 20,
            searchResultLimit: 20,
            itemSelectText: 'Press to select',
        });
    });
});
