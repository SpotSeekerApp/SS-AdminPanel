
function toggleCheckbox(selectedCheckbox) {
  const checkboxes = document.getElementsByName('userType');
  checkboxes.forEach(checkbox => {
    if (checkbox.id !== selectedCheckbox) {
      checkbox.checked = false;
    }
  });
}