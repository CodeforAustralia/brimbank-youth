$(function () {

var loadForm = function () {
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-contact").modal("show");
      console.log(btn.attr("data-url"));
    },
    success: function (data) {
      $("#modal-contact .modal-content").html(data.html_form);
    }
  });
};

var loadForm2 = function () {
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-sms").modal("show");
      console.log(btn.attr("data-url"));
    },
    success: function (data) {
      $("#modal-sms .modal-content").html(data.html_form);
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
        $('[data-toggle="tooltip"]').tooltip();
      }
      else {
        $("#modal-group .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

var copyGroup = function () {
  var btn = $(this);
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $("#group").html(data.html_group_list);
      $('.info-tooltip').tooltip();
    }
  });
};

var getActivityList = function () {
  var btn = $(this);
  var activityList, emailList, mobileNoList;
  var activitiesArr, activitiesArr2 = [];
  var sms_url, email_url, activity_url_final;
  var ori_url = (window.location.href).toString();
  var web_url = (ori_url.substr(0, ori_url.indexOf('?')));
  var ori_url_2 = (ori_url.substr(0, ori_url.indexOf('#')));
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data, event) {
      activitiesArr = $('#id_activities').val(); // retrieve selected activities

      // Codes for Mailgun/Twilio sharing
      activityList = activitiesArr.join('_');
      emailList = data.email_list.join(';');
      mobileNoList = data.mobileno_list.join(';');
      if (activityList != '') {
          sms_url = web_url + "sms_create/" + activityList + "/";
          email_url = web_url + "email_create/" + activityList + "/";
      } else {
          sms_url = "#";
          email_url = "#";
      }
      // ---- END ---- Codes for Mailgun/Twilio sharing

      // Codes for default email client / mobile text sharing
      if (web_url != '') {
        activity_url = web_url + "activity/detail/";
      } else {
          if ( ori_url_2 != '' ){
              activity_url = ori_url_2 + "activity/detail/";
          } else {
              activity_url = ori_url + "activity/detail/";
          }
      }
      if (activitiesArr != []) {
        activitiesArr.forEach(function(element) {
          activitiesArr2.push(activity_url + element + "/");
        });
      }

      if (activitiesArr != []) {
        activity_url_final = activitiesArr2.join('%0D%0A');
      }

      if (activity_url_final != '') {
          email_url = "mailto:?subject=Check%20these%20out&to="+ emailList+ "&body=Check these out:%0D%0A" + activity_url_final;
          sms_url = "sms:?&to=" + mobileNoList + "&body=Check%20these%20out:%20" + activity_url_final;
      } else {
          email_url = "mailto:?subject=Check%20these%20out&&to=" + emailList + "&body=Check these out:%0D%0A";
          sms_url = "sms:?&to=" + mobileNoList + "body=Check%20these%20out:%20";
      }
      // ---- END ------ Codes for default email client / mobile text sharing
      window.open(email_url);
      window.open(sms_url);
    }
  });
  return false;
};

var getActivityListContacts = function () {
  var btn = $(this);
  var activityList, email, mobileNo;
  var activitiesArr, activitiesArr2 = [];
  var sms_url, email_url, activity_url_final;
  var ori_url = (window.location.href).toString();
  var home_url = (window.location.hostname).toString();
  if (home_url == 'localhost') {
    home_url = "http://localhost:8000/";
  } else {
    home_url = "http://" + home_url + "/";
  }
  var web_url = (ori_url.substr(0, ori_url.indexOf('?')));
  var ori_url_2 = (ori_url.substr(0, ori_url.indexOf('#')));
  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data, event) {
      activitiesArr = $('#id_activities').val(); // retrieve selected activities
      // Codes for Mailgun/Twilio sharing
      activityList = activitiesArr.join('_');
      email = data.email;
      mobileNo = data.mobile_no;
      if (activityList != '') {
          sms_url = home_url + "sms_create/" + activityList + "/";
          email_url = home_url + "email_create/" + activityList + "/";
      } else {
          sms_url = "#";
          email_url = "#";
      }
      // ---- END ---- Codes for Mailgun/Twilio sharing

      // Codes for default email client / mobile text sharing
      // if (web_url != '') {
      //   activity_url = web_url + "activity/detail/";
      // } else {
      //     if ( ori_url_2 != '' ){
      //         activity_url = ori_url_2 + "activity/detail/";
      //     } else {
      //         activity_url = ori_url + "activity/detail/";
      //     }
      // }
      // if (activitiesArr != []) {
      //   activitiesArr.forEach(function(element) {
      //     activitiesArr2.push(activity_url + element + "/");
      //   });
      // }

      // if (activitiesArr != []) {
      //   activity_url_final = activitiesArr2.join('%0D%0A');
      // }

      // if (activity_url_final != '') {
      //     email_url = "mailto:?subject=Check%20these%20out&to="+ email+ "&body=Check these out:%0D%0A" + activity_url_final;
      //     sms_url = "sms:?&to=" + mobileNo + "&body=Check%20these%20out:%20" + activity_url_final;
      // } else {
      //     email_url = "mailto:?subject=Check%20these%20out&&to=" + email + "&body=Check these out:%0D%0A";
      //     sms_url = "sms:?&to=" + mobileNo + "body=Check%20these%20out:%20";
      // }
      // ---- END ------ Codes for default email client / mobile text sharing
      window.open(email_url, 'newwindow', 'width=500,height=900');
      window.open(sms_url, 'newwindow', 'width=500,height=900');
    }
  });
  return false;
};

var shareActivitiesContacts = function () {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    beforeSend: function () {
      console.log(form.attr("action"));
      $('.loading').show();
    },
    success: function (data) {
      if (data.form_is_valid) {
        $("#modal-contact").modal("hide");
      }
      else {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

var shareActivitiesContacts2 = function () {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    beforeSend: function () {
      console.log(form.attr("action"));
      $('.loading').show();
    },
    success: function (data) {
      if (data.form_is_valid) {
        $("#modal-sms").modal("hide");
      }
      else {
        $("#modal-sms .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};

// ------ NEW ------

// Copy contact group
// $(".copy-group-btn").click(copyGroup);
$(document).on('click', '.copy-group-btn', copyGroup);

// Share activities to group
$(document).on('click', '.share-activities-btn', loadGroupForm);
// $("#modal-contact").on("submit", ".share-activities-form", getActivityList);
$(document).on('click', '.share-btn', getActivityList);

// Share activities to contacts (EMAIL)
$(document).on('click', '.share-activities-btn-contacts', loadForm);
$("#modal-contact").on("submit", ".share-activities-form", shareActivitiesContacts);

// Share activities to contacts (SMS)
$(document).on('click', '.share-activities-btn-contacts-sms', loadForm2);
$("#modal-sms").on("submit", ".share-activities-sms-form", shareActivitiesContacts2);

// Create Email group
$(".js-create-email-group").click(loadGroupForm);
$(document).on('click', '.js-create-email-group', loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-create-form", saveGroupForm);

// Update Email group
$("#group").on("click", ".js-update-email-group",loadGroupForm);
$(document).on('click', '.js-update-email-group', loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-update-form",saveGroupForm);

// Delete Email group
$("#group").on("click", ".js-delete-email-group", loadGroupForm);
$(document).on('click', '.js-delete-email-group', loadGroupForm);
$("#modal-group").on("submit", ".js-email-group-delete-form", saveGroupForm);


// Create SMS group
$(".js-create-group").click(loadGroupForm);
$("#modal-group").on("submit", ".js-group-create-form", saveGroupForm);

// Update SMS group
$("#group").on("click", ".js-update-sms-group",loadGroupForm);
$("#modal-group").on("submit", ".js-sms-group-update-form",saveGroupForm);

// Delete SMS group
$("#group").on("click", ".js-delete-sms-group", loadGroupForm);
$("#modal-group").on("submit", ".js-sms-group-delete-form", saveGroupForm);
  
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