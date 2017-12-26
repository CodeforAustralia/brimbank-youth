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
    $("#modal-signup").modal("hide");
    $("#modal-progress").modal("show");
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      // progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      //   var progress = parseInt(data.loaded / data.total * 100, 10);
      //   var strProgress = progress + "%";
      //   $(".progress-bar").css({"width": strProgress});
      //   $(".progress-bar").text(strProgress);
      // },
      success: function (data) {
        if (data.form_is_valid) {
//        $("#message_list").html(data.messages2);
        $("#modal-progress").modal("hide");
        $("#modal-confirmation").modal("show");
        // $("#modal-progress").modal("hide");
        }
        else {
          $("#modal-signup .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });