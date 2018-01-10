$(function () {

    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
        //   $("#modal-share-url").modal("show");
        alert("test");
        },
        success: function (data) {
          $("#modal-share-url .modal-content").html(data.html_form);
        }
      });
    };
    
    // Display share-url modal
    // $(".js-share-url").click(loadForm);

    // $("#modal-group").on("submit", ".js-group-create-form", saveGroupForm);
    
});