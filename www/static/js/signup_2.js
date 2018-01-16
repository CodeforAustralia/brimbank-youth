$(function () {
    $(".js-signup").click(function () {
      $.ajax({
        url: '/signup_ajax_form/',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-signup").modal("show");
        },
        success: function (data) {
          $("#modal-signup .modal-content").html(data.html_form);
        }
      });
    });
  
  });
  
  $("#modal-signup").on("submit", ".js-signup-submit", function () {
      var form = $(this);
      var data = form.serialize();
      var data_split = data.split("&");
      var a;

      if ((data_split[1] == "username=") || (data_split[2]=="email=") || (data_split[3]=="password1=")|| (data_split[4]=="password2=")){
        $("#modal-progress").modal("hide");
      }

      $.ajax(
        {
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            a = 1;
            // alert(data.user_pk);
            $("#modal-progress").modal("hide");
            $("#modal-signup").modal("hide");
            $("#modal-confirmation").modal("show");
            window.location.href = "/create_profile/" + data.user_pk;
          }
          else {
              a = 0;
              $("#modal-progress").modal("hide");
              $("#modal-signup").modal("show");
              $("#modal-signup .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    });