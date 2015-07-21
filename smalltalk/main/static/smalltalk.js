$( document ).ready(function() {

    $("#new_contact_button").click(function(e) {
        $("#contact_form_container").show();
    });

    $("#new_group_button").click(function(e) {
        $("#group_form_container").show();
    });

    $("#new_contact_submit").click(new_contact_submit);

    $("#new_group_submit").click(new_group_submit);

    $("#manage_group_submit").click(update_group_manager);

    $("#manage_contact_submit").click(update_contact_manager);
});

function update_contact_manager() {

    var input_dict = [];
    $("#id_contacts").find("input[type=checkbox]").each(function() {
        input_dict.push({pk: $(this).val(), checked: $(this).prop('checked')});
    })

    $.ajax({
        url: '/update_contact_manager',
        type: 'POST',
        data: {'contact_manage_form': JSON.stringify(input_dict),
        'contacted_object_type': $("#object-details").attr("object-type"),
        'contacted_object_pk': $("#object-details").attr("object-pk")},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            $("#contact_list").empty()
            for (var key in data['current_contacts']) {
                contact = data['current_contacts'][key];
                html_string = "<a href='" + contact['url'] + "'>" + contact['name'] + "</a> ";
                $("#contact_list").append(html_string)
            };
        },
        error: function (response) {
            $("#contact_list").empty();
            $("#contact_list").append("There was an error updating this group's contacts.");
        }
    });
};

function update_group_manager() {

    var input_dict = [];
    $("#id_groups").find("input[type=checkbox]").each(function() {
        input_dict.push({pk: $(this).val(), checked: $(this).prop('checked')});
    })

    $.ajax({
        url: '/update_group_manager',
        type: 'POST',
        data: {'group_manage_form': JSON.stringify(input_dict),
            'grouped_object_type': $("#object-details").attr("object-type"),
            'grouped_object_pk': $("#object-details").attr("object-pk")},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            $("#group_list").empty()
            for (var key in data['current_groups']) {
                group = data['current_groups'][key];
                html_string = "<a href='" + group['url'] + "'>" + group['name'] + "</a> ";
                $("#group_list").append(html_string)
            };
        },
        error: function (response) {
            $("#group_list").empty();
            $("#group_list").append("There was an error updating this contact's groups.");
        }
    });
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
