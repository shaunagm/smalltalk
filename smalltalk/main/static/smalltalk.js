$( document ).ready(function() {

    $("#new_contact_button").click(function(e) {
        $("#contact_form_container").show();
    });

    $("#new_group_button").click(function(e) {
        $("#group_form_container").show();
    });

    $('#new_contact_submit').click(function() {

        $.ajax({
            url: '/new_contact',
            type: 'POST',
            data: {'name': $("#id_contact-name").val(),
                'details': $("#id_contact-details").val()},
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(data, textStatus, jqXHR) {
                var d = $.parseJSON(data);
                if (d.status == "success") {
                    $("#contact_form_container").hide();
                    $("#new_contact_message").html("You have added a new contact: <a href='" +
                        d.url + "'>" + d.name + "</a>.");
                } else {
                    $("#new_contact_message").html(d.message);
                }
            },
            error: function (response) {
                console.log(response);
                $("#new_contact_message").html("There was an error with the site.");
            }
        });

    });

    $('#new_group_submit').click(function() {

        $.ajax({
            url: '/new_group',
            type: 'POST',
            data: {'name': $("#id_group-name").val(),
            'details': $("#id_group-details").val()},
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(data, textStatus, jqXHR) {
                var d = $.parseJSON(data);
                if (d.status == "success") {
                    $("#group_form_container").hide();
                    $("#new_group_message").html("You have added a new group: <a href='" +
                    d.url + "'>" + d.name + "</a>.");
                } else {
                    $("#new_group_message").html(d.message);
                }
            },
            error: function (response) {
                console.log(response);
                $("#new_group_message").html("There was an error with the site.");
            }
        });

    });

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
