
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

    // Initialization step to display tags received from Flask as initially selected options
    const initialTags = document.querySelector('.modaledit .selected-options-list');

    if (initialTags.value != 0) {
      let initialTagsList = initialTags.value.split(',')

      const selectedOptionsContainer = initialTags.parentNode.querySelector('.selected-options');

      initialTagsList.forEach(tag => {
        const optionElement = document.createElement('div');
        optionElement.classList.add('selected-option');
        optionElement.dataset.value = tag;
        optionElement.innerHTML = `
          <span>${tag}</span>
          <span class="remove-option">X</span>
        `;
        
        selectedOptionsContainer.appendChild(optionElement);

        optionElement.querySelector('.remove-option').addEventListener('click', function() {
          const formElement = optionElement.parentNode.parentNode

          optionElement.remove();

          console.log("formElement", formElement)
          formElement.querySelectorAll('.selected-options-list').value =  Array.from(formElement.querySelectorAll('.selected-option'))
              .map(option => option.dataset.value).join(',');
          

          // console.log(hiddenInput,"final value of tags")

          //  hiddenInput_final = formElement.querySelectorAll('.selected-options-list');
          // hiddenInput_final = hiddenInput

          console.log(formElement, "formElement")
              
        });
      });
    }

    // selectedOptionsContainer.appendChild(optionElement);


    // main code to handle dropdown select
    const selectors = document.querySelectorAll('.tagSelect');
    selectors.forEach(select => {
      
      select.addEventListener('change', function(e) {

        // select container(div) to add selected tags as buttons
        const selectedOptionsContainer = select.parentNode.querySelector('.selected-options');
        
        // console.log("selectedOptionsContainer main", selectedOptionsContainer)

        // select hidden input(input) to store selected tags as string 
        const hiddenInput = select.parentNode.querySelector(".selected-options-list");

        // console.log("hiddeninput main", hiddenInput)
        
        const selectedOption = e.target.options[e.target.selectedIndex];
        const selectedValue = selectedOption.value;
        const selectedText = selectedOption.text;

        // all selected options 
        const existingOptions = select.parentNode.querySelectorAll('.selected-option');
        let isAlreadySelected = false;
  
        existingOptions.forEach(option => {
          if (option.dataset.value === selectedValue) {
            isAlreadySelected = true;
          }
        });
        
        if (!isAlreadySelected) {
            const optionElement = document.createElement('div');

            optionElement.classList.add('selected-option');
            optionElement.dataset.value = selectedValue;
            optionElement.innerHTML = `
                <span>${selectedText}</span>
                <span class="remove-option">X</span>
            `;

            selectedOptionsContainer.appendChild(optionElement);
  
            optionElement.querySelector('.remove-option').addEventListener('click', function() {
                optionElement.remove();

                // Remove value from hidden input
                hiddenInput.value = Array.from( select.parentNode.querySelectorAll('.selected-option'))
                    .map(option => option.dataset.value).join(',');
                    
            });
        }
            
        // Update hidden input with new selected value
        const selectedValues = Array.from( select.parentNode.querySelectorAll('.selected-option'))
            .map(option => option.dataset.value);

        hiddenInput.value = selectedValues.join(',');
      });

    });

      
});
  