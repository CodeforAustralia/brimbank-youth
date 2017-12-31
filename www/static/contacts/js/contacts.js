$(function () {

var loadForm = function () {
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-contact").modal("show");
    },
    success: function (data) {
      $("#modal-contact .modal-content").html(data.html_form);
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
    success: function (data) {
      if (data.form_is_valid) {
        $("#contact-table tbody").html(data.html_sms_member_list);
        $("#modal-contact").modal("hide");
      }
      else {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};
  
// Create SMS contact
$(".js-create-sms-member").click(loadForm);
$("#modal-contact").on("submit", ".js-sms-member-create-form", saveForm);

// Update SMS contact
$("#contact-table").on("click", ".js-update-sms-member",loadForm);
$("#modal-contact").on("submit", ".js-sms-member-update-form",saveForm);

// Delete contact
$("#contact-table").on("click", ".js-delete-sms-member", loadForm);
$("#modal-contact").on("submit", ".js-sms-member-delete-form", saveForm);

});