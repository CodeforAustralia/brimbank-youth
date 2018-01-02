$(function () {

var markActivity = function () {
    var btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function (data) {
            // alert(btn.attr("id"));
        },
        // success: function (data) {
        // $("#modal-group .modal-content").html(data.html_form);
        // }
    });
    // return false;
};

// Mark an activity
// $(".js-bookmark-article").click(markActivity);

});