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
    let messageSpan = document.createElement('span')

    const email = emailInput.value;
    const password = passInput.value;
    if (password.length < 6) {
        let flashMessage = 'Password must be at least 6 characters long';
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
            else if (response.data.email_not_verified) {
                console.log(response.data.message);

            //} 
            // else if (response.data.emailVerified !== null && !response.data.emailVerified) {
            //     console.log("Error during login", response.data.message)
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

    // Create an input field for the email
    let emailInput = document.createElement('input');
    emailInput.type = 'email';
    emailInput.id = 'emailInput';
    emailInput.placeholder = 'Enter your email';

    // Create a submit button
    let submitButton = document.createElement('button');
    submitButton.innerHTML = 'Submit';
    // Get the resetDiv
    let resetDiv = document.getElementById('resetDiv');
    // Append the input field and the button to the div
    resetDiv.appendChild(emailInput);
    resetDiv.appendChild(submitButton);

    // // Append the div to the body of the document
    // document.body.appendChild(resetDiv);

    // Add an event listener to the submit button
    submitButton.addEventListener('click', function() {
        const email = emailInput.value;
        if (email) {
            // Send a POST request to the backend
            axios.post('/api/reset', {email: email})
            .then(function(response) {
                let resetEmailSent = document.createElement('span');
                let resetConfirm = document.getElementById('resetConfirm')
                resetEmailSent.textContent = response.data.message;
                resetConfirm.appendChild(resetEmailSent).style.backgroundColor = 'lightblue';
            })
            .catch(function(error) {
                console.error("Error resetting password:", error);
            });
        }
    });
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
