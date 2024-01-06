
/*password query selector.*/
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');


/*SHOW PASSAWORD */ 
togglePassword.addEventListener('click', function() {
    const text = password.getAttribute('type') === 'password' ? 'text' : 'password';
    console.log("text", text);
    password.setAttribute('type', text);
    
    // Toggle the eye and bi-eye icon
    togglePassword.classList.toggle('bi-eye');
    togglePassword.classList.toggle('bi-eye-slash');
});


/*SUBMIT BUTTON SUCCESSFUL MESAGE*/
document.addEventListener("DOMContentLoaded", function(){

        
    const alert_submit_button = document.getElementById("alert-button");   
    const alert_message=document.getElementById("successMessage");
    

    alert_submit_button.addEventListener('click', function(event){

        event.preventDefault();

        alert_message.style.display = "block";

        setTimeout(function(){
            alert_message.style.display = "none";
        }, 3000);
        
    });
   
});
