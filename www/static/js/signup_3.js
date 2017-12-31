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
      alert($("#show_progress").value());

      if ((data_split[1] == "username=") || (data_split[2]=="email=") || (data_split[3]=="password1=")|| (data_split[4]=="password2=")){
        $("#modal-progress").modal("hide");
      }
      else{
        // if ($("#show_progress").value() == "True"){
        $("#modal-progress").modal("show");
      }
    //   }
      alert(data);

      $.ajax(
        {
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#modal-progress").modal("hide");
            $("#modal-signup").modal("hide");
            $("#modal-confirmation").modal("show");
          }
          else {
            // alert(data.no_progress_display);
            // $("#show_progress").html("False");
            // if(data.no_progress_display){
            $("#modal-progress").modal("hide");
            $("#modal-signup").modal("show");
            $("#modal-signup .modal-content").html(data.html_form);
            // }
          }
        }
      });
      return false;
    });