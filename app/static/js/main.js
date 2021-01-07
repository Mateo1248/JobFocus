var error_panel = false;
var curr_date = new Date().getFullYear();

$(document).ready(function() {
    if (typeof message !== 'undefined') {
        $("#alert_message").html(message);
        $("#alert_custom").css('display', 'block');
    }
    else {
        $("#alert_custom").css('display', 'none');
    }

    $("#alert_exit").click(function (e) {
        $("#alert_custom").slideToggle(300);
        error_panel = false;
    });

    $('#scrollTop').click(function(e) {
        $('#main').scrollTop(0);
        console.log("elo")
    });

    $('#main').scroll( function() {
        console.log("scrl  eloo")
        if ($('#main').scrollTop() > 20) {
            $('#scrollTop').css({
                display:"block"
            });
        } else {
            $('#scrollTop').css({
                display:"none"
            });
        }
    });
});

function error_show(error_msg) {
    $("#alert_message").html(error_msg);
    if(!error_panel) {
        $("#alert_custom").slideToggle(300);
    }
    error_panel = true;
}

function error_close() {
    if(error_panel) {
        $("#alert_custom").slideToggle(300);
    }
    error_panel = false;
}

function formToDict(serialized_array) {
    res = Object();
    serialized_array.forEach(function(el) {
        res[el.name] = el.value;
    });
    return res;
}

function validate(form_data, form) {

    var email_re = /\S+@\S+\.\S+/; /** any@any.any */
    var pass_re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/; /** min 6 signs one lower case and one upper case letter */
    var str_re = /[a-zA-Z]*[a-zA-Z]/
    var year_re = /[0-9]{4}/
    var bd_re = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/
    var error_msg = "";
    var error = false;
    var BreakException = {};

    try {
        form_data.forEach(function(el) {
            var value = el.value;

            switch (el.name) {
                case "email":
                    if (!email_re.test(value)) {
                        error_msg = "Wrong email!";
                        error = true;
                        throw BreakException;
                    }
                    break;
                case "password":
                    if (!pass_re.test(value)) {
                        error_msg = "Password must contain numbers, upper and lower case letters and its length should be more than 6 characters!";
                        error = true;
                        throw BreakException;
                    }
                    break;
                case "firstname":
                case "city":
                case "surname":
                    if (!str_re.test(value)) {
                        error_msg = "First name, surname and city should be non empty and contain only small or capital letters!";
                        error = true;
                        throw BreakException;
                    }
                    break;
                case "birth_year":
                    if (!year_re.test(value) || parseInt(value) < 1900 || parseInt(value) > curr_date) {
                        error_msg = "Birth year should be number between 1900 and "+ curr_date +"!";
                        error = true;
                        throw BreakException;
                    }
                    break;

                case "birth_date":

                    if (!bd_re.test(value)) {
                        error_msg = "Birth date should be in format YYYY-MM-DD!";
                        error = true;
                        throw BreakException;
                    }
                    break;
            }
        });
    } catch (e) {
        if (e !== BreakException) throw e;
    }

    if (error) {
        error_show(error_msg);
        form.preventDefault();
        return false;
    }
    return true;
}

function loader_start() {
    $(document.body).append(
        "<div id=\"loader_cont\"><div id=\"loader_cust\"></div></div>"
    )
};

function loader_stop() {
    $('#loader_cont').remove();
};
