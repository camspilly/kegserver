$(document).ready(function() {
  $("#cardError").hide()
// using jQuery

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $("#registerButton").on("click", function() {
    $("#registerForm").submit();
  });

  $("#loginButton").on("click", function() {
    $("#loginForm").submit();
    window.location.href = "/account";
  });


  $("#removePaymentInfoBtn").on("click", function() {
    $("#removePaymentForm").submit()
  });

  $("#addPaymentInfoBtn").on("click", function() {
    var $form = $("#creditCardForm");

    // Disable the submit button to prevent repeated clicks
    $form.find('button').prop('disabled', true);

    Stripe.card.createToken($form, function(status, response) {
      if (status == 200) {
        $.ajax({
          beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }},

          type: "POST",
          url: '/account/add_payment',
          data: response
        });

        $("#cardError").hide()
        window.location.href = "/account";
      } else {
        $("#cardError").show()
      }
    });

    // Prevent the form from submitting with the default action
    return false;
  });
});
