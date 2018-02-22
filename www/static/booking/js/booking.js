var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-register").modal("show");
      },
      success: function (data) {
        $("#modal-register .modal-content").html(data.html_form);
        if (data.fully_booked) {
          $("#modal-register").modal("hide");
          location.reload();
        }
      }
    });
};

var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend: function () {
          $('.loading').show();
      },
      success: function (data) {
        $('.loading').hide();
        if (data.form_is_valid) {
          $("#modal-register").modal("hide");
          $("#contact-table").html(data.attendee_list);
          $("#attendees_no").html(data.attendees_no);
          $("#available_space").html(data.available_space);
          $("#send-reminder-btn").html(data.send_reminder_btn);
          $('[data-toggle="tooltip"]').tooltip();
        }
        else {
          $("#modal-register .modal-content").html(data.html_form);
        }
      }
    });
    return false;
};

var saveYouthForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            $(".js-booking-youth-form")[0].reset();
            $(".confirm-register").text("Registered !");
            $(".confirm-register").attr("disabled", "disabled");
        }
        else {
          $(".js-booking-youth-form")[0].reset();
          $("#modal-register .modal-content").html(data.html_form);
        }
      }
    });
    return false;
};

// Youth registers to an activity
$(document).on('click', '.register', loadForm);
$("#modal-register").on("submit", ".js-booking-youth-form", saveYouthForm);

// Youth worker registers client to an activity
$(document).on('click', '.js-register-client', loadForm);
// $(".js-register-client").click(loadForm);
$("#modal-register").on("submit", ".js-booking-form", saveForm);