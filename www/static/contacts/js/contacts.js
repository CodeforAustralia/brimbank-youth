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
  // var group_id = "#table_" + form.attr("id") + " tbody";
  $.ajax({
    url: form.attr("action"),
    // url: '/sms_members/' + form.attr("id") + '/create/',
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        // change id of contact-table into {{ group.id }} [DONE]
        // change URL of sms_member_create to include group.pk
        // change sms_member_create function in views.py to receive group.pk
        
        // $("#contact-table tbody").html(data.html_sms_member_list);
        $('#contact-list').html(data.html_sms_member_list);
        $("#modal-contact").modal("hide");
      }
      else {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

var modifyDeleteForm = function () {
  var form = $(this);
  var group_id = "#table_" + form.attr("id") + " tbody";
  $.ajax({
    url: form.attr("action"),
    // url: '/sms_members/' + form.attr("id") + '/create/',
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $(group_id).html(data.html_sms_member_list);
        $("#modal-contact").modal("hide");
      }
      else {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

var loadGroupForm = function () {
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-group").modal("show");
    },
    success: function (data) {
      $("#modal-group .modal-content").html(data.html_form);
    }
  });
};

var saveGroupForm = function () {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#group").html(data.html_group_list);
        $("#modal-group").modal("hide");
      }
      else {
        $("#modal-group .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

// Create SMS group
$(".js-create-group").click(loadGroupForm);
$("#modal-group").on("submit", ".js-group-create-form", saveGroupForm);

// Update SMS group
$("#group").on("click", ".js-update-sms-group",loadGroupForm);
$("#modal-group").on("submit", ".js-sms-group-update-form",saveGroupForm);

// Delete SMS group
$("#group").on("click", ".js-delete-sms-group", loadGroupForm);
$("#modal-group").on("submit", ".js-sms-group-delete-form", saveGroupForm);

// Create Email group
$(".js-create-email-group").click(loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-create-form", saveGroupForm);

// Update Email group
$("#group").on("click", ".js-update-email-group",loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-update-form",saveGroupForm);

// Delete Email group
$("#group").on("click", ".js-delete-email-group", loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-delete-form", saveGroupForm);
  
// Create SMS contact
$(".js-create-sms-member").click(loadForm);
$(document).on('click', '.js-create-sms-member', loadForm);
$("#modal-contact").on("submit", ".js-sms-member-create-form", saveForm);

// Update SMS contact
$("#contact-table").on("click", ".js-update-sms-member",loadForm);
$("#modal-contact").on("submit", ".js-sms-member-update-form",saveForm);

// Delete contact
// $("#contact-table").on("click", ".js-delete-sms-member", loadForm);
$(".contact").on("click", ".js-delete-sms-member", loadForm);
$(document).on('click', '.js-delete-sms-member', loadForm);
// $("#modal-contact").on("submit", ".js-sms-member-delete-form", saveForm);
$("#modal-contact").on("submit", ".js-sms-member-delete-form", modifyDeleteForm);

// Create Email contact
$(".js-create-email-member").click(loadForm);
$(document).on('click', '.js-create-email-member', loadForm);
$("#modal-contact").on("submit", ".js-email-member-create-form", saveForm);

// Update Email contact
$("#contact-table").on("click", ".js-update-email-member",loadForm);
$("#modal-contact").on("submit", ".js-email-member-update-form",saveForm);

// Delete Email contact
$("#contact-table").on("click", ".js-delete-email-member", loadForm);
$(document).on('click', '.js-delete-email-member', loadForm);
$("#modal-contact").on("submit", ".js-email-member-delete-form", saveForm);

});