
document.addEventListener("DOMContentLoaded", function () {

  const onboardingForm = document.getElementById("onboarding");

  if (onboardingForm) {
    const nameInput = document.getElementById("name");
    const usernameInput = document.getElementById("username");
    const usernameExists = document.getElementById("usernameExists");
    const nextButton1 = document.getElementById("nextButton1");
    const nextButtonName = document.getElementById("nextButtonName");
    const nextButtonUsername = document.getElementById("nextButtonUsername");
    const nextButtonDob = document.getElementById("nextButtonDob");
    const nextButtonCountry = document.getElementById("nextButtonCountry");
    let currentPage = 1;

    // Add event listeners only if the elements exist
    if (nextButton1) nextButton1.addEventListener("click", nextPage);
    if (nextButtonName) nextButtonName.addEventListener("click", () => validateAndProceed("name"));
    if (nextButtonUsername) nextButtonUsername.addEventListener("click", () => validateAndProceed("username"));
    if (nextButtonDob) nextButtonDob.addEventListener("click", nextPage);
    if (nextButtonCountry) nextButtonCountry.addEventListener("click", nextPage);
    if (nameInput) nameInput.addEventListener("input", checkInputs);
    if (usernameInput) {
      usernameInput.addEventListener("input", () => {
        validateUsername(usernameInput.value.trim(), checkInputs);
      });
    }


// Validate fields and navigate
function validateAndProceed(fieldId) {
  const input = document.getElementById(fieldId);
  const value = input.value.trim();

  if (fieldId === "name" && !value) {
    alert("Please provide your name.");
    return;
  }

  if (fieldId === "username") {
    validateUsername(value, (isValid) => {
      if (isValid) {
        nextPage();
      } else {
        alert("Username already exists. Please choose a different one.");
      }
    });
    return;
  }

  nextPage();
}


function validateUsername(username, callback) {
  if (!username) {
    usernameExists.textContent = "Username is required.";
    usernameExists.classList.remove("d-none");
    usernameExists.style.color = "red";
    callback(false);
    return;
  }

  axios.post("/validate_username", { username: username })
    .then((response) => {
      if (response.data.exists) {
        usernameExists.textContent = "Username already exists.";
        usernameExists.classList.remove("d-none");
        usernameExists.style.color = "red";
        callback(false);
      } else {
        usernameExists.textContent = "";
        usernameExists.classList.add("d-none");
        callback(true);
      }
    })
    .catch((error) => {
      console.error("Error validating username:", error);
      usernameExists.textContent = "An error occurred. Try again.";
      usernameExists.classList.remove("d-none");
      usernameExists.style.color = "red";
      callback(false);
    });
}

// Proceed to the next page
function nextPage() {
  const currentElement = document.querySelector(`[data-page="${currentPage}"]`);
  if (currentElement) currentElement.classList.add("hidden");

  currentPage++;

  const nextElement = document.querySelector(`[data-page="${currentPage}"]`);
  if (nextElement) nextElement.classList.remove("hidden");
}

// Enable/disable the final button based on inputs
function checkInputs() {
  if (nameInput.value.trim() && !usernameExists.textContent && usernameInput.value.trim()) {
    doneButton.disabled = false;
  } else {
    doneButton.disabled = true;
  }
}

// Form submission
onboardingForm.addEventListener("submit", (event) => {
  if (!onboardingForm.checkValidity()) {
    event.preventDefault();
    alert("Please complete all required fields.");
  } else {
    console.log("Form is valid, submitting...");
    event.preventDefault();
    onboarding();
  }
});

} 
// else {
//   console.log("Onboarding script loaded, but this is not the onboarding page.");
//}

});

// Function to validate username for update form
function validateUsername_update(username, callback) {
  // const username = usernameInput.value.trim().toLowerCase();
  if (username !== '') {
    axios.post('/validate_username', {username: username})
    .then(function (response) {
      if (response.data.exists) {
        
        // Username already exists
        usernameExists.textContent = "Username exists.";
        usernameExists.classList.remove('d-none');
        usernameExists.style.display =  'block';
        
        // format message
        usernameExists.style.color = 'red'; 
        usernameExists.style.fontWeight = 'bold'; 
        usernameExists.style.fontSize = '1.2em'; 
        callback(false);
        
      } else {
        // Username is available
        usernameExists.textContent = "";
        usernameExists.classList.add('d-none');
        callback(true); // Username is valid, submit data

        // Recheck if done button should be enabled
        if (document.getElementById('onboarding')) {
          checkInput();
        }
        
      }
    })
    .catch(function (error) {
      // Handle specific username validation errors
      console.error("Error during username validation", error);

      // Clear any previous sucess messages and hide them
      usernameExists.textContent = "";
      usernameExists.classList.add('d-none');
    });
  } else {
    // Handle cases where username is empty
    usernameExists.textContent = "";
    usernameExists.classList.add("d-none");
    if (doneButton) {
      doneButton.disabled = true;
    }
    callback(false);
  }
}

// // Form submission
// document.addEventListener('DOMContentLoaded', function() {
// // Add event listener to the form submission
//   const onboardingForm = document.getElementById('onboarding');
//   // Event listener to enable/disbale 'Done button based on name and username
//   const nameInput = document.getElementById('name');
//   const usernameInput = document.getElementById('username');
//   const doneButton = document.getElementById('doneButton');
  
//   // Function to check if user has provided name and username
//   function checkInput() {
//     if (nameInput.value.trim() !== '' && usernameInput.value.trim() !=='') {
//       doneButton.disabled = false;
//     } else {
//       doneButton.disabled = true;
//     }
//   }

  
//  // Function to validate username
//  function validateUsername() {
//   const username = usernameInput.value.trim().toLowerCase();
//   if (username !== '') {
//     axios.post('/validate_username', {username:username})
//     .then(function (response) {
//       if (response.data.exists) {

//         // Username already exists
//         usernameExists.textContent = "Username exists.";
//         usernameExists.classList.remove('d-none');

//         // format message
//         usernameExists.style.color = 'red'; 
//         usernameExists.style.fontWeight = 'bold'; 
//         usernameExists.style.fontSize = '1.2em'; 

//       } else {
//         // Username is available
//         usernameExists.textContent = "";
//         usernameExists.classList.add('d-none');
//         // Recheck if done button should be enabled
//         checkInput();
//       }
//     })
//     .catch(function (error) {
//       // Handle specific username validation errors
//       console.error("Error during username validation", error);

//       // Clear any previous sucess messages and hide them
//       usernameExists.textContent = "";
//       usernameExists.classList.add('d-none');
//     });
//   } else {
//     // Handle cases where username is empty
//     usernameExists.textContent = "";
//     usernameExists.classList.add("d-none");
//     doneButton.disabled = true;
//   }
// }

//   // Validate form and call onboarding function
//   if (onboardingForm) {
//       nameInput.addEventListener('input', checkInput);
//       usernameInput.addEventListener('input', validateUsername);

//       onboardingForm.addEventListener('submit', function(event) {

//         // Check form validity
//         if (!onboardingForm.checkValidity()) {
//             console.log("Form is not valid");
//         } else {
//           // Prevent default form submission behavior
//           event.preventDefault(); 
//           // Form is valid, proceed with submission 
//           console.log("Form is valid.")
//           // Call onboarding function when form is submitted
//           onboarding();  
//         }   
//     });
//   }
// });

// Profile picture upload
    // Upload button for profile picture
    const uploadForm = document.getElementById('uploadForm')
    if (uploadForm) {
      uploadForm.addEventListener('submit', function(event) {

        // Prevent default form submission
        event.preventDefault();

        let file = document.getElementById('profilePic').files[0];
        const uploadResponse = document.getElementById('uploadError');

        // Clear any previous error messasge
        uploadResponse.textContent = '';

        // Check if a file is selected
        if (!file) {
          uploadResponse.textContent = "No file selected";
          console.error("No file selected");
          return;
        }

        // Validate file type
        const validImageType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!validImageType.includes(file.type)) {
          uploadResponse.textContent = "Invalid file type. Please select an image file(jpeg, png, gif)."
          uploadResponse.style.color = 'red';
          console.error('Invalid file type. Please select an image file(jpeg, png, gif).');
          return;
        }

        // If the file is valid, proceed with the upload
        let formData = new FormData();
        formData.append('profilePic', file);
  
        axios.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(function(response) {
          uploadResponse.style.color = 'green';
          uploadResponse.textContent = response.data.message;
          // Clear the file input field
          document.getElementById('profilePic').value = '';
          console.log(response);
        })
        .catch(function(error) {
          uploadResponse.textContent = 'Error uploading file';
          console.error('Error uploading file', error);
        });
      });
    }


  // Profile Data update
  const editButtons = document.querySelectorAll('.edit-btn');
  const saveButtons = document.querySelectorAll('.save-btn');
  const ethnicityOptions =  document.getElementById('ethnicity-options');
  const ethnicityInput = document.getElementById('ethnicityInput');
  const cancelButtons = document.querySelectorAll('.cancel-btn');


  // Special function to update input field with selected checkboxes
  const checkboxes = document.querySelectorAll('input[type="checkbox"][name="ethnicity"]');

  // Event listener for checkboxes
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        updateInputField(); // Update input fiels when checkbox state changes
      });
    });  

  // Function to update input field with selected checkboxes
  function updateInputField() {
    const selectedEthnicities = [];
    checkboxes.forEach(checkbox => {
      if (checkbox.checked) {
        selectedEthnicities.push(checkbox.value);
      }
    });
    // Update input with selected values
    if (ethnicityInput) {
      ethnicityInput.value = selectedEthnicities.join(', ');
    }
    
  }

  editButtons.forEach(editButton => {
      editButton.addEventListener('click', function(event) {
        event.preventDefault();
          const field = this.getAttribute('data-field');
          const inputElement = document.getElementById(`${field}Input`);
          const selectElement = document.getElementById(`${field}Select`);
          const saveButton = document.querySelector(`.save-btn[data-field="${field}"]`);
          const cancelButton = document.querySelector(`.cancel-btn[data-field="${field}"]`);

          if (inputElement && saveButton && cancelButton) {
              inputElement.disabled = false; // Enable input field
              this.classList.add('d-none'); // Hide Edit button
              saveButton.classList.remove('d-none'); // Show Save button
              cancelButton.classList.remove('d-none'); // Show Cancel button
              if (field === 'ethnicity') {
                ethnicityOptions.style.display = 'block' // Show ethnicity options
              }
              
          }
      });
  });

  saveButtons.forEach(saveButton => {
      saveButton.addEventListener('click', function(event) {
          event.preventDefault(); // Prevent default form submission
          const field = this.getAttribute('data-field');
          const inputElement = document.getElementById(`${field}Input`);
          const editButton = document.querySelector(`.edit-btn[data-field="${field}"]`);
          const ethnicityOptions =  document.getElementById('ethnicity-options');
          const cancelButton = document.querySelector(`.cancel-btn[data-field="${field}"]`);
          const saveButton = document.querySelector(`.save-btn[data-field="${field}"]`);

          // Validate input if required
          if (field === "name" || field === "username") {
            if (inputElement.value.trim() === '') {
              inputElement.classList.add('is-invalid');
              const missingInput = document.getElementById(`${field}Error`);
              console.log(missingInput)
              missingInput.textContent = "Please provide a value";
              missingInput.style.display = "block";
              usernameExists.style.display =  'none';
              missingInput.style.color = 'red'; 
              missingInput.style.fontWeight = 'bold'; 
              missingInput.style.fontSize = '1.2em'; 
              return;
            } else {
              inputElement.classList.remove('is-invalid');
              const missingInput = document.getElementById(`${field}Error`);
              missingInput.textContent = "";
              missingInput.style.display =  'none';
              usernameExists.style.display =  'none';
            }
          }

          if (inputElement) {
            if (field === 'username') {
              validateUsername_update(inputElement.value, function (isValid) {
                if (isValid) {
                  updateProfile(field, inputElement.value, inputElement, saveButton, editButton, cancelButton);
                }
              });
            } else {
              updateProfile(field, inputElement.value, inputElement, saveButton, editButton, ethnicityOptions, cancelButton);
            }
          }

              
      });
  });
  cancelButtons.forEach(cancelButton => {
    cancelButton.addEventListener('click', function(event) {
      event.preventDefault(); // Prevent default action
      const field = this.getAttribute('data-field');
      const inputElement = document.getElementById(`${field}Input`);
      //const selectElement = document.getElementById(`${field}Select`);
      const editButton = document.querySelector(`.edit-btn[data-field="${field}"]`);
      const saveButton = document.querySelector(`.save-btn[data-field="${field}"]`);
  
      if (inputElement && editButton && saveButton) {
        inputElement.disabled = true; // Disable input field
        inputElement.value = inputElement.getAttribute('placeholder'); // Reset input field value
        this.classList.add('d-none'); // Hide Cancel button
        saveButton.classList.add('d-none'); // Hide Save button
        editButton.classList.remove('d-none'); // Show Edit button
        if (field === 'ethnicity') {
          ethnicityOptions.style.display = 'none'; // Hide ethnicity options
        }
      }
    });
  });

  // variables for drop-down select options
  const editSelections = document.querySelectorAll('.edit-selection');
  const updateSelections = document.querySelectorAll('.update-selection');
  const cancelSelections = document.querySelectorAll('.cancel-selection');

  // Activate selection field, hide edit btn and unhide save and cancel
  editSelections.forEach(editSelection => {
    editSelection.addEventListener('click', function(event) {
        event.preventDefault();
        const field = this.getAttribute('data-field');
        const form = this.closest('form'); // Get the closest form element
        const selectElement = form.querySelector(`#${field}Selection`);

        if (selectElement) {
            selectElement.disabled = false;
            this.classList.add('d-none');

            // Handle nodelist for saveselections and cancelselections within the same form
            form.querySelectorAll(`.update-selection[data-field="${field}"]`).forEach(updateSelection => {
                updateSelection.classList.remove('d-none');
            });
            form.querySelectorAll(`.cancel-selection[data-field="${field}"]`).forEach(cancelSelection => {
                cancelSelection.classList.remove('d-none');
            });
        }
    });
});

  updateSelections.forEach(updateSelection => {
    updateSelection.addEventListener('click', function(event) {
      event.preventDefault();
      const field = this.getAttribute('data-field');
      const selectElement = document.getElementById(`${field}Selection`);
      const editSelection = document.querySelectorAll(`.edit-selection[data-field="${field}"]`);
      const updateSelection = document.querySelectorAll(`.update-selection[data-field="${field}"]`);
      const cancelSelection = document.querySelectorAll(`.cancel-selection[data-field="${field}"]`);

      if (selectElement) {
        const value = selectElement.value;
        updateProfile(field, value, selectElement, updateSelection, cancelSelection, editSelection)
      }
    })
  })

  cancelSelections.forEach(cancelSelection => {
    cancelSelection.addEventListener('click', function(event) {
        event.preventDefault();
        const field = this.getAttribute('data-field');
        const form = this.closest('form'); // Get the closest form element
        const selectElement = form.querySelector(`#${field}Selection`);
        const editSelection = form.querySelectorAll(`.edit-selection[data-field="${field}"]`);
        const updateSelection = form.querySelectorAll(`.update-selection[data-field="${field}"]`);
        const cancelSelection = form.querySelectorAll(`.cancel-selection[data-field="${field}"]`);

        if (selectElement && editSelection && updateSelection && cancelSelection) {
            selectElement.disabled = true;
            editSelection.forEach(editSel => editSel.classList.remove('d-none'));
            updateSelection.forEach(updSel => updSel.classList.add('d-none'));
            cancelSelection.forEach(cancelSel => cancelSel.classList.add('d-none'));
        }
    });
});

  // Send profile update data to flask backend
function updateProfile(field, 
    value, 
    inputElement, 
    saveButton, 
    editButton, 
    ethnicityOptions, 
    cancelButton,
    selectElement, 
    updateSelection, 
    cancelSelection, 
    editSelection
  ) {

  axios.post('/edit_profile', { [field]: value })
  .then(response => {
      console.log(response.data.message); // Log success message
      // Handle button reset
      editButtons.forEach(editButton => {
        editButton.classList.remove('d-none');
      });
      saveButtons.forEach(saveButton => {
        saveButton.classList.add('d-none');
      });
      cancelButtons.forEach(cancelButton => {
        cancelButton.classList.add('d-none');
      });
      inputElement.disabled = true; // Disable input field after saving
      if (field === 'ethnicity') {
        // Hide ethnicity options
        ethnicityOptions.style.display = 'none';
      } 
      // Handle select option reset
      editSelections.forEach(editSelection => {
        editSelection.classList.remove('d-none');
      });
      updateSelections.forEach(updateSelection => {
        updateSelection.classList.add('d-none');
      });
      cancelSelections.forEach(cancelSelection => {
        cancelSelection.classList.add('d-none');
      })
      // Disable select field after saving
      if (selectElement) {
        selectElement.disabled = true;
      }
  })
  .catch(error => {
      console.error('Error saving data', error); // Handle error
      // Optionally show error message
  });
}

// Onboarding
function onboarding() {
  // Code to fetch personal info
  const username = document.getElementById('username').value;
  const name = document.getElementById('name').value;
  const country = document.getElementById("countrySelect").value;
  const dob = document.getElementById('dob').value;
  
  const formData = {
      username: username,
      name:name,
      country:country,
      dob:dob
  };
  const formDataJsonString = JSON.stringify(formData);
  try {
    const parsedData = JSON.parse(formDataJsonString);
    console.log("Valid JSON:", parsedData);
  } catch (error) {
    console.error("Invalid JSON:", error);
  }
  // Submit form
  if (username && name && country) {
    axios.post('/onboarding', formDataJsonString, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function(response) {
      // Perform the redirect
      if (response.data.redirect_url) {
        //
        window.location.href = response.data.redirect_url;
        console.log(response.data.message);
      } else {
        // Handle the case where there is no redirect URL
        console.error("Error during onboarding: ", response.data.message);
      }
    })
    .catch(function (error) {
      console.error("Error during onboarding", error);
    });
  } else {
    console.error("Missing required fields");
  }
}