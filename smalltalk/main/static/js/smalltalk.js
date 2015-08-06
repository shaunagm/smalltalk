$( document ).ready(function() {

    // Datatable (for list objects)
    var oTable = $('#object_list_table').dataTable({
        "paging":   false,
        "info":     false,
        "aoColumnDefs": [
            { 'bVisible': false, 'aTargets': [1,2,3,4] }
        ],
        "aaSorting": []
    });

    $('#list_table_alpha').click(function(){
        oTable.fnSort([  [0,'asc']] );
    });

    $('#list_table_recent').click(function(){
        oTable.fnSort([  [1,'desc']] );
    });

    $('#list_table_contacts').click(function(){
        oTable.fnSort([  [2,'desc']] );
    });

    $('#list_table_groups').click(function(){
        oTable.fnSort([  [3,'desc']] );
    });

    $('#list_table_topics').click(function(){
        oTable.fnSort([  [4,'desc']] );
    });

    $('#inline_contact_div #filter_options').keyup(function (){
        process_fuse_text_match('#inline_contact_div');
    });

    $('#inline_group_div #filter_options').keyup(function (){
        process_fuse_text_match('#inline_group_div');
    });

    $('#inline_topic_div #filter_options').keyup(function (){
        process_fuse_text_match('#inline_topic_div');
    });

    $("#new_contact_button").click(function(e) {
        $("#contact_form_container").show();
    });

    $("#new_group_button").click(function(e) {
        $("#group_form_container").show();
    });

    $("#new_contact_submit").click(new_contact_submit);

    $("#new_group_submit").click(new_group_submit);

    $(".manager-button").click(function(){
        toggle_manage_button(this);
    });

    $(".view_archived_button").click(function(){
        view_archived_toggle(this);
    });

    $("#manage_group_submit").click(function() {
        update_manager("group");
    });

    $("#manage_contact_submit").click(function () {
        update_manager("contact");
    });

    $("#manage_topic_submit").click(function () {
        update_manager("topic");
    });

});


function append_topic(item, write_element){

    var data = {
        "name": item['name'],
        "url": item['url'],
        "pk": item['pk'],
        "global_text": "this topic and all items with this topic",
        "local_text": "just the topic (will not affect items already connected to this topic)"
    };

    if (item['archived'] == true ) {
        data["archive_keyword"] = "unarchive";
        data["archive_glyphicon"] = "glyphicon-upload";
    } else {
        data["archive_keyword"] = "archive";
        data["archive_glyphicon"] = "glyphicon-download";
    };

    if (item['starred'] == true ) {
        data["star_keyword"] = "unstar";
        data["star_glyphicon"] = "glyphicon-star";
    } else {
        data["star_keyword"] = "star";
        data["star_glyphicon"] = "glyphicon-star-empty";
    };

    var dataTemplate;

    $.get("http://" + document.location.host + "/static/html_templates/topic_inline.txt", function(value) {
        dataTemplate = $.templates(value);
        var html = dataTemplate.render(data);
        $(write_element).append(html);
    });

}



function toggle_topic(toggle_type, toggle_scope, topic_pk) {
    // This function is called directly from the template (see topic_icons.html)

    $.ajax({
        url: '/toggle-topic',
        type: 'POST',
        data: { 'toggle_type': toggle_type, 'toggle_scope': toggle_scope, 'topic_pk': topic_pk,
            'object_type': $("#object-details").attr("object-type"),
            'object_pk': $("#object-details").attr("object-pk"),},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            var d = $.parseJSON(data);
            var star_selector = "#star-" + topic_pk;
            var archive_selector = "#archive-" + topic_pk;
            if (d['topic_data']['starred'] == true) {
                $(star_selector + " a span").addClass('glyphicon-star').removeClass('glyphicon-star-empty');
                $(star_selector + " div.star-keyword").each(function () {
                    $(this).text("un-star");
                });
            } else {
                $(star_selector + " a span").addClass('glyphicon-star-empty').removeClass('glyphicon-star');
                $(star_selector + " div.star-keyword").each(function () {
                    $(this).text("star");
                });
            };

            if (d['topic_data']['archived'] == true) {
                $(archive_selector + " a span").addClass('glyphicon-upload').removeClass('glyphicon-download');
                $(archive_selector + " div.archive-keyword").each(function () {
                    $(this).text("un-archive");
                });
            } else {
                $(archive_selector + " a span").addClass('glyphicon-download').removeClass('glyphicon-upload');
                $(archive_selector + " div.archive-keyword").each(function () {
                    $(this).text("archive");
                });
            };
        },
        error: function (response) {
        }});
}

function view_archived_toggle(elem) {
    if (elem.getAttribute("toggle-state") ==  "off") {
        elem.setAttribute("toggle-state", "on");
        elem.textContent = "Hide Archived";
        $(".archived-object").show();
    } else {
        elem.setAttribute("toggle-state", "off");
        $(".archived-object").hide();
        elem.textContent = "Show Archived";
    };
}

function toggle_manage_button(elem) {
    if (elem.getAttribute("toggle-state") ==  "off") {
        elem.setAttribute("toggle-state", "on");
        elem.textContent = "Close";
        $(elem).parent().parent().children('.inline_div').show();
    } else {
        elem.setAttribute("toggle-state", "off");
        elem.textContent = "Manage";
        $(elem).parent().parent().children('.inline_div').hide();
    };
}

function process_fuse_text_match(input_text_field) {
    // Takes the name of the containing div and creates an array of items to search through.
    var search_array = []
    $('label', $(input_text_field + " form ul")).each(function () {
        search_array.push({'html_id': $(this).children("input").attr('id'),
            'name': $(this).text() });
    });

    // Takes the search text input name, and creates a search item.
    var search_text = $(input_text_field + " #filter_options").val();

    if(search_text.replace(/\s/g,"") == ""){
        $('li', $(input_text_field + " form ul")).show();  // Show all
    } else {
        // Gets array of matching items using Fuse.
        var f = new Fuse(search_array, {keys: ['name']});
        var result = f.search(search_text);

        // Alters HTML so viewer can see matching items.
        $('li', $(input_text_field + " form ul")).hide();
        result.forEach(function(item) {
            $("#" + item.html_id).parents("li").show();
        });
    };
}

function update_manager(object_type_to_adjust) {

    if (object_type_to_adjust == "group") {
        var read_element = "#id_groups";
        var write_element = "#group_list";
        var error_message = "There was an error updating groups";
    };

    if (object_type_to_adjust == "contact") {
        var read_element = "#id_contacts";
        var write_element = "#contact_list";
        var error_message = "There was an error updating contacts.";
    };

    if (object_type_to_adjust == "topic") {
        var read_element = "#id_topics";
        var write_element = "#topic_list";
        var error_message = "There was an error updating topics.";
    };

    var input_dict = [];
    $(read_element).find("input[type=checkbox]").each(function() {
        input_dict.push({pk: $(this).val(), checked: $(this).prop('checked')});
    });
    console.log(JSON.stringify(input_dict));

    $.ajax({
        url: '/update_manager',
        type: 'POST',
        data: {'manage_form': JSON.stringify(input_dict),
        'object_type_to_adjust': object_type_to_adjust,
        'object_type': $("#object-details").attr("object-type"),
        'object_pk': $("#object-details").attr("object-pk")},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            $(write_element).empty()
            for (var key in data['current_dict']) {
                item = data['current_dict'][key];
                if (object_type_to_adjust == "topic") {
                    append_topic(item, write_element);
                } else {
                    $(write_element).append("<a href='" + item['url'] + "'>" + item['name'] + "</a> ");
                };
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
