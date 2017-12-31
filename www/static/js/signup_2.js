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

      // setTimeout(function(){ 
      //   if (a!=1){
      //     $("#modal-progress").on('shown.bs.modal', function () {
      //       $("#modal-progress").modal("hide") && $("#modal-signup").modal("show");
      //     });
      //   } 
      // }, 3000);
      if ((data_split[1] == "username=") || (data_split[2]=="email=") || (data_split[3]=="password1=")|| (data_split[4]=="password2=")){
        $("#modal-progress").modal("hide");
      }
      // else{
      //   alert("test");
      //   $("#modal-progress").modal("show") && $("#modal-signup").modal("hide");
      // }

      $.ajax(
        {
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            a = 1;
            $("#modal-progress").modal("hide");
            $("#modal-signup").modal("hide");
            $("#modal-confirmation").modal("show");
            
          }
          else {
            // if ($('#modal-progress').hasClass('show')){
              // alert("test2");
              a = 0;
              $("#modal-progress").modal("hide");
              $("#modal-signup").modal("show");
              // $("#modal-progress").removeClass("show") && $("#modal-signup").addClass("show");
              // $("#modal-signup").modal("show");
              // break
            // }
            // $("#modal-progress").modal("hide");
            // $("#modal-progress").removeClass("show");
            // $("#modal-signup").modal("show");
            // $("#modal-signup").addClass("show");
            // $("#modal-progress").on('shown.bs.modal', function () {
              // alert("test");
              // $("#modal-progress").modal("hide") && $("#modal-signup").modal("show");
            // });
            // if ($('#modal-progress').hasClass('show')){
              // $("#modal-progress").removeClass('show');
              // $("#modal-progress").modal("hide");
              // $("#modal-signup").modal("show");
              //alert("test");
              // $("#modal-signup").modal("show");
              // $("#modal-progress").removeClass("show");
              // $("#modal-progress").css("display", "none");
            // }
            // else{
            //   alert("test2");
            //   $("#modal-signup").modal("show") && $("#modal-progress").modal("hide");
            // }
            $("#modal-signup .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    });