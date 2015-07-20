$( document ).ready(function() {

    $("#new_contact_button").click(function(e) {
        $("#contact_form_container").show();
    });

    $("#new_group_button").click(function(e) {
        $("#group_form_container").show();
    });

    $("#new_contact_submit").click(new_contact_submit);

    $("#new_group_submit").click(new_group_submit);

    $("#load_group_manager").click(load_group_manager);

    $("#update_group_manager").click(update_group_manager);


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

function load_group_manager() {

    $.ajax({
        url: '/load_group_manager',
        type: 'POST',
        data: {'name': $("#contact_name").text()},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            $("#manage_group_prompt").show();
            $("#update_group_manager").show()
            $("#inline_group_div").html('<div class="btn-group" data-toggle="buttons">');
            var d = $.parseJSON(data);
            for (var key in d.data) {
                var group = d.data[key];
                group_html =  '<label class="btn btn-primary active">' +
                    '<input type="checkbox" autocomplete="off" class="group_input"';
                if (group['in_group'] == 1 ) {
                    group_html += " checked";
                }
                group_html += '>' + group['group_name'] +'</label>';
                $("#inline_group_div").append(group_html);
            };
            $("#inline_group_div").append("</div>");
        },
        error: function (response) {
            console.log(response);
        }});
};

function create_dict_from_form(selector) {
    var input_dict = [];
    $(selector).each(function() {
        input_dict.push({key: $(this).parent().text(), value: $(this).prop('checked')});
    });
    return input_dict;
};

function update_group_manager() {

    $.ajax({
        url: '/update_group_manager',
        type: 'POST',
        data: {'group_list' : JSON.stringify(create_dict_from_form(".group_input"))},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            console.log("success");
        },
        error: function (response) {
            console.log(response);
        }});
};



function new_contact_submit() {

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
        }});
};

function new_group_submit() {

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
        }});

};
