$(document).ready(function () {
  // Use form name not button
  $("#loginFrm").submit(function (e) {
    // Get all of the data from the login form
    e.preventDefault();
    const logFormData = $("#loginFrm").serialize();
    alert(logFormData)
    let csrfToken = getCookie("csrftoken");

    $.ajax({
      type: "POST",
      url: "/",
      data: logFormData,
      header: { "X-CSRFToken": csrfToken },
      success: function (data) {
        // When all errors are resolved the dictionary will return just

        if (data["user_id"] > 0) {
          // Set the text to null for all error messages and remove blink class
          // iterate over the errorNamesID and remove blink class and text
          alert(data)
          $("#password-email-login-err").text("");
          $("#password-email-login-err").removeClass("blink");

          window.location.href = "http://127.0.0.1:8000/index/";
        } else {
          alert(data['log-email-nm'])
          $("#password-email-login-err").text(data["no-match-password"]);
          $("#password-email-login-err").addClass("blink");
        }
      },
    });
  });


// get the csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = jQuery.trim(cookies[i]);
      // let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
});



// let csrfToken = getCookie("csrftoken");
// const loginFrm = document.querySelector('#loginFrm')

// loginFrm.onsubmit = async (e) => {
//   const logEmail = document.querySelector('#log-email').value;
//   const logPassword = document.querySelector('#log-password').value;
//   formData = {
//     'log-email-nm' : logEmail,
//     'log-password-nm' : logPassword,
//   }
  
//     e.preventDefault();
//     alert(formData)
//     try {
//         let response = await fetch("/", {
//             method: 'POST',
//             credentials: 'same-origin', // required
//             headers: {
//                 'Accept-Type': 'application/json',
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrfToken,
//                 'X-Requested-With': 'XMLHttpRequest',
//             },
//             body: JSON.stringify(formData)
//     });
//             // let data = await response.json();
//             let data = await response.json();
//             console.log(data);

//     } catch (error) {
//            console.log('****ERROR MESSAGE****'); 
//            console.log(error);
//     }   
// }