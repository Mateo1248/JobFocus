$(document).ready(function() {
    var ph = $(".rightBox").height()
    $(".empCT").css({
        height: ""+ph - ($(".empCB").outerHeight())
    });


    $('#userDetails').submit(function (e) {

        if (deleteB) {
            var jqxhr = $.ajax({
                method: "DELETE",
                url: "/user",
            })
            .done(function(response) {
                window.location.replace("/auth");
                error_show("User succesfully deleted!");
            })
            .fail(function(response) {
                error_show("Something went wrong!")
            });
            e.preventDefault();
        }
        else {
            validate(
                $('#userDetails').serializeArray(),
                e
            );
        }
    });


    $('#empInter').submit(function(e) {
        sendForm(
            "/user/employee/interest",
            "POST",
            "#empInter",
            e
        )
        .done(function(response) {
            error_show("Interest added succesfully!");
        })
        .fail(function(response) {
            error_show("Can't add interest!");
        });
    });


    $('#empExp').submit(function(e) {
        sendForm(
            "/user/employee/experience",
            "POST",
            "#empExp",
            e
        )
        .done(function(response) {
            error_show("Experience added succesfully!");
        })
        .fail(function(response) {
            error_show("Can't add experience, city does not exists!");
        });
    });


    $('#jobOffer').submit(function(e) {
        sendForm(
            "/user/employeer/advert",
            "POST",
            "#jobOffer",
            e
        )
        .done(function(response) {
            error_show("New job offer added succesfully!");
        })
        .fail(function(response) {
            error_show("Can't add job offer!");
        });
    });
});


function sendForm(url, method, formId, e) {
    e.preventDefault();
    var jqxhr = $.ajax({
        method: method,
        url: url,
        data: $(formId).serialize()
    });
    return jqxhr
}