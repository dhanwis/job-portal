(function($) {

	"use strict";


})(jQuery);

// Add this script at the end of your HTML file or in a separate JS file

// Toggle Password Visibility

document.getElementById("passwordInput").addEventListener("input", function() {
    var passwordInput = document.getElementById("passwordInput");
    if (passwordInput.type === "text") {
        passwordInput.type = "password";
        document.getElementById("togglePassword").querySelector("i").classList.toggle("fa-eye-slash");
    }
});

document.getElementById("togglePassword").addEventListener("click", function() {
    var passwordInput = document.getElementById("passwordInput");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
    this.querySelector("i").classList.toggle("fa-eye-slash");
});


// Sign In with Google Button
document.getElementById("signInGoogle").addEventListener("click", function() {
    // Redirect or perform Google sign-in process here
    // Example: window.location.href = "https://accounts.google.com";
});
