$(function() {
  let $step1 = $('.wrap').eq(0);
  let $step2 = $('.wrap').eq(1);
  let $step3 = $('.wrap').eq(2);
  let $content = $('#content');
  let $thanks = $('#content-thanks');
  let $dashboard = $('#content-dashboard');
  let countrySelected = false;
  
  // select2 hook
  $('.select2-selects').select2();

  function setFirstBtn() {
    let  $checks = $step1.find('.ga-checkbox');
    if (countrySelected && $step1.find('.ga-checkbox:checked').length == $checks.length) {
       $step1.find('.btn-first').prop('disabled', false);
    } else {
      $step1.find('.btn-first').prop('disabled', true);
    }
  }

  // enable on select change
  $step1.find('.select-country').change(function(e) {
    countrySelected = true
    setFirstBtn()
  });

  $step1.find('.ga-checkbox').eq(0).change(function(e) {
    setFirstBtn()
  });

  $step1.find('.ga-checkbox').eq(1).change(function(e) {
    setFirstBtn()
  });

  // hide all
  $('.wrap').addClass('hidden');

  // open first
  $step1.removeClass('hidden');

  // on step 1 button continue
  $step1.find('.click').click(function(e) {
    $step1.addClass('hidden');
    $step2.removeClass('hidden');

    // check off
    $step1.addClass('complete').find('.state-icon').text('');
  });

  // on step 2 button continue
  $step2.find('.click').click(function(e) {
    $step2.addClass('hidden');
    $step3.removeClass('hidden');

    // check off
    $step2.addClass('complete').find('.state-icon').text('');
  });

  // on step 3 button continue
  // $step3.find('.click').click(function(e) {
  //   $content.hide();
  //   $thanks.fadeIn();
  // });
    

});

// Onboarding form submission
document.addEventListener('DOMContentLoaded', function() {
// Add event listener to the form submission
  const onboardingForm = document.getElementById('onboarding');
  // Event listener to enable/disbale 'Done button based on name and username
  const nameInput = document.getElementById('name');
  const usernameInput = document.getElementById('username');
  const doneButton = document.getElementById('doneButton');
  
  // Function to check if user has provided name and username
  function checkInput() {
    if (nameInput.value.trim() !== '' && usernameInput.value.trim() !=='') {
      doneButton.disabled = false;
    } else {
      doneButton.disabled = true;
    }
  }

  // Function to validate username
  function validateUsername() {
    const username = usernameInput.value.trim().toLowerCase();
    if (username !== '') {
      axios.post('/validate_username', {username:username})
      .then(function (response) {
        if (response.data.exists) {
          
          // Username already exists
          usernameExists.textContent = "Username already exists.";
          usernameExists.classList.remove('hidden');
          
          // format message
          usernameExists.style.color = 'red'; 
          usernameExists.style.fontWeight = 'bold'; 
          usernameExists.style.fontSize = '1.2em'; 

          doneButton.disabled = true;
        } else {
          // Username is available
          usernameExists.textContent = "";
          usernameExists.classList.add('hidden');
          // Recheck if done button should be enabled
          checkInput();
        }
      })
      .catch(function (error) {
        // Handle specific username validation errors
        console.error("Error during username validation", error);

        // Clear any previous sucess messages and hide them
        usernameExists.textContent = "";
        usernameExists.classList.add('hidden');
      });
    } else {
      // Handle cases where username is empty
      usernameExists.textContent = "";
      usernameExists.classList.add("hidden");
      doneButton.disabled = true;
    }
  }



  if (onboardingForm) {
      nameInput.addEventListener('input', checkInput);
      usernameInput.addEventListener('input', validateUsername);

      onboardingForm.addEventListener('submit', function(event) {

        // Check form validity
        if (!onboardingForm.checkValidity()) {
            console.log("Form is not valid");
        } else {
          // Prevent default form submission behavior
          event.preventDefault(); 
          // Form is valid, proceed with submission 
          console.log("Form is valid.")
          // Call onboarding function when form is submitted
          onboarding();  
        }   
    });
  }
});

// Onboarding
function onboarding() {
  // Code to fetch personal info
  const username = document.getElementById('username').value;
  const name = document.getElementById('name').value;
  const country = document.getElementById("countrySelect").value;
  const dob = document.getElementById('dob').value;
  const gender = document.getElementById('gender').value;
  const ethnicity = Array.from(document.querySelectorAll('input[name="ethnicity"]:checked')).map(checkbox => checkbox.value);
  // Collect selected ethnicitied
  // const ethnicity = [];
  // document.querySelector('input[name="ethnicity"]:checked').forEach((checkbox) => {
  //   selectedEthnicities.push(checkbox.value);
  // });

  // Proffesional info
  const industry = document.getElementById('industry').value;
  const jobFunction = document.getElementById("jobFunction").value;
  const seniority = document.getElementById('seniority').value;
  const salary = document.getElementById("salary").value;
  const education = document.getElementById("education").value;
  
  // Submit form
  if (username && name && country) {
    axios.post('/onboarding', {
      username: username,
      name:name,
      country:country,
      dob:dob,
      gender:gender,
      ethnicity:ethnicity,
      industry:industry,
      jobFunction:jobFunction,
      seniority:seniority,
      salary: salary,
      education: education
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
  }
}

