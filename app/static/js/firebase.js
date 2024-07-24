document.addEventListener('DOMContentLoaded', function() {
    // fetchTodos();
    
    // // Add event listener to the form submission
    let signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission behavior
            signup(); // Call signup function when form is submitted
        });
    }

    let loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission behavior
            login(); // Call login function when form is submitted
        });
    }
    let logoutTrigger = document.getElementById('logout');
    if (logoutTrigger) {
        logoutTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission behavior
            logout(); // Call login function on button click
        });
    }
    let resetTrigger = document.getElementById('reset');
    if (resetTrigger) {
        resetTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission behavior
            reset(); // Call reset function on-click
        });
    }
    

});

function signup() {
    let emailInput = document.getElementById('signup-email');
    let passInput = document.getElementById('signup-password');
    let emailExists = document.getElementById('emailExists');
    let messageSpan = document.createElement('span');
    let passInputRepeat = document.getElementById('signup-password-repeat')

    while (emailExists.firstChild) {
        emailExists.removeChild(emailExists.firstChild);
    }
    const email = emailInput.value;
    const password = passInput.value;
    const passwordRepet = passInputRepeat.value;

    if (password.length < 6) {
        let flashMessage = 'Password must be at least 6 characters long';
        messageSpan.textContent = flashMessage;
        emailExists.appendChild(messageSpan);
        return;
    } 
    if (password != passwordRepet) {
        let flashMessage = 'Passwords Do not match';
        messageSpan.textContent = flashMessage;
        emailExists.appendChild(messageSpan);
        return;
    }
    if (email && password) {
        axios.post('/api/signup', {email: email, password: password})
        .then(function(response) {
           // Check if the response contains a redirect URL
           if (response.data.redirect_url) {
                // Perform the redirect
                window.location.href = response.data.redirect_url;
                console.log(response.data.message);
            } else {
                // Handle the case where there is no redirect URL
                console.error("Error during signup: ", response.data.message);
                messageSpan.textContent = response.data.message;
                emailExists.appendChild(messageSpan);
            }

        })
        .catch(function (error) {
            console.error("Error during signup: ", error);
        });
    }

    
}

function login() {
    let emailInput = document.getElementById('l-email');
    let passInput = document.getElementById('l-password');
    let messageDiv = document.getElementById('flashMessage');
    // Remove existing child (if any)
    while (messageDiv.firstChild) {
        messageDiv.removeChild(messageDiv.firstChild);
    }

    let span = document.createElement('span');



    const email = emailInput.value;
    const password = passInput.value;

    if (email && password) {
        axios.post('/api/login', {email: email, password: password})
        .then(function(response) {
            if (response.data.redirect_url) {
                // Perform the redirect
                window.location.href = response.data.redirect_url;
                console.log(response.data.message);
            } 
            else {
                // Handle the case where there is no redirect URL
                console.error("Error during login: ", response.data.message);
                span.textContent = response.data.message;
                messageDiv.appendChild(span);

            }

        })
        .catch(function (error) {
            console.error("Error during login: ", error);
        });
    } else {
        console.error("Email or password is missing");
    }
}

function reset() {
    let submitButton = document.getElementById('submit-button');
    let emailInput = document.getElementById('emailInput-reset');

    // Ensure that the event listener is not added multiple times
    submitButton.removeEventListener('click', handleReset);

    submitButton.addEventListener('click', handleReset);

    function handleReset() {
        const email = emailInput.value;
        if (email) {
            console.log(email);
            // Send a POST request to the backend
            axios.post('/api/reset', {email: email})
                .then(function(response) {
                    let resetEmailSent = document.createElement('span');
                    let resetConfirm = document.getElementById('resetConfirm');
                    resetEmailSent.textContent = response.data.message;
                    resetConfirm.innerHTML = ''; // Clear previous messages
                    resetConfirm.appendChild(resetEmailSent);
                    resetConfirm.style.fontSize = '1.2em'; 
                    resetConfirm.style.fontWeight = 'bold'; 
                    resetConfirm.style.color = 'blue'; 
                })
                .catch(function(error) {
                    let resetConfirm = document.getElementById('resetConfirm');
                    let errorMessage = document.createElement('span');
                    errorMessage.textContent = error.response.data.Message || 'An error occurred while resetting the password';
                    resetConfirm.innerHTML = ''; // Clear previous messages
                    resetConfirm.appendChild(errorMessage);
                    resetConfirm.style.fontSize = '1.2em'; 
                    resetConfirm.style.fontWeight = 'bold'; 
                    resetConfirm.style.color = 'red'; 
                    console.error("Error resetting password:", error);
                });
        }
    }
}


function logout ()  {
    axios.get('/api/logout')
    .then(function(response) {
        window.location.href = response.data.redirect_url;
    })
    .catch(function(error) {
        console.error("Error during logout:", error);
    })
}

// Delete user
// document.addEventListener('DOMContentLoaded', function() {
//     const deleteBtn = document.getElementById('delete-user-btn');

//     if (deleteBtn) {
//         deleteBtn.addEventListener('click', function(event) {
//             event.preventDefault();
//             let passwordInput= document.getElementById("delete-password-input");
//             const deletepassword = passwordInput.value;

//             if (password) {
//                 axios.post('/api/delete_user', { password: deletepassword })
//                     .then(function(response) {
//                         if (response.data.success) {
//                             alert(response.data.message);
//                             // Redirect to the home page or login page after deletion
//                             window.location.href = '/';
//                         } else {
//                             alert(response.data.message);
//                         }
//                     })
//                     .catch(function(error) {
//                         console.error("Error during user deletion", error);
//                         alert("Error during user deletion: " + error.response.data.message);
//                     });
//             }
//         });
//     }
// });

// Activate delete account
document.addEventListener('DOMContentLoaded', function() {
    const deleteBtn = document.getElementById('delete-user-btn');
    const confirmDeleteCheckbox = document.getElementById('confirm-delete-checkbox');
    const passwordInput = document.getElementById('delete-password-input');
    const feedbackDiv = document.getElementById('delete-feedback');

    if (confirmDeleteCheckbox) {
      confirmDeleteCheckbox.addEventListener('change', function() {
        deleteBtn.disabled = !this.checked;
      });
    }

    if (deleteBtn) {
      deleteBtn.addEventListener('click', function(event) {
        event.preventDefault();
        const password = passwordInput.value;

        if (password) {
          axios.post('/api/delete_user', { password: password })
            .then(function(response) {
              if (response.data.success) {
                feedbackDiv.innerHTML = '<div class="alert alert-success">' + response.data.message + '</div>';
                setTimeout(function() {
                  window.location.href = response.data.redirect_url;
                }, 2000);
              } else {
                feedbackDiv.innerHTML = '<div class="alert alert-warning">' + response.data.message + '</div>';
              }
            })
            .catch(function(error) {
              console.error("Error while deleting user data", error);
              feedbackDiv.innerHTML = '<div class="alert alert-danger">' + error.response.data.message + '</div>';
            });
        } else {
          feedbackDiv.innerHTML = '<div class="alert alert-warning">Password is required.</div>';
        }
      });
    }
  });
// function googlePopup() {
//     signInWithPopup(auth, provider)
//         .then((result) => {
//             // This gives you a Google Access Token. You can use it to access the Google API.
//             const credential = GoogleAuthProvider.credentialFromResult(result);
//             const token = credential.accessToken;
//             // The signed-in user info.
//             const user = result.user;
//             // IdP data available using getAdditionalUserInfo(result)
//             // ...
//         }).catch((error) => {
//             // Handle Errors here.
//             const errorCode = error.code;
//             const errorMessage = error.message;
//             // The email of the user's account used.
//             const email = error.customData.email;
//             // The AuthCredential type that was used.
//             const credential = GoogleAuthProvider.credentialFromError(error);
//             // ...
//         });
// }
