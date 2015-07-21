$( document ).ready(function() {

    $("#new_contact_button").click(function(e) {
        $("#contact_form_container").show();
    });

    $("#new_group_button").click(function(e) {
        $("#group_form_container").show();
    });

    $("#new_contact_submit").click(new_contact_submit);

    $("#new_group_submit").click(new_group_submit);

    $("#manage_group_submit").click(update_manager);

    $("#manage_contact_submit").click(update_manager);
});

function update_manager() {

    var object_type = $("#object-details").attr("object-type");

    if (object_type == "Group") {
        var read_element = "#id_contacts";
        var write_element = "#contact_list";
        var error_message = "There was an error updating this group's contacts.";
    };

    if (object_type == "Contact") {
        var read_element = "#id_groups";
        var write_element = "#group_list";
        var error_message = "There was an error updating this contact's groups";
    };

    var input_dict = [];
    $(read_element).find("input[type=checkbox]").each(function() {
        input_dict.push({pk: $(this).val(), checked: $(this).prop('checked')});
    });

    $.ajax({
        url: '/update_manager',
        type: 'POST',
        data: {'manage_form': JSON.stringify(input_dict),
        'object_type': object_type,
        'object_pk': $("#object-details").attr("object-pk")},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            $(write_element).empty()
            for (var key in data['current_dict']) {
                item = data['current_dict'][key];
                $(write_element).append("<a href='" + item['url'] + "'>" + item['name'] + "</a> ");
            };
        },
        error: function (response) {
            $(write_element).empty();
            $(write_element).append(error_message);
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
