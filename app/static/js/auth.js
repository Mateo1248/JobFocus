$(document).ready(function() {
    $("#yearPicker").attr({
        "max" : new Date().getFullYear(),
        "min" : 1900
     });

    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });

    const employeeRadio = document.getElementById('employeeRadio');
    const employeerRadio = document.getElementById('employeerRadio');
    const signUpSubmitButton = document.getElementById('signUpSubmit');

    employeeRadio.addEventListener('click', () => {
        signUpSubmitButton.textContent="CONTINUE...";
    });

    employeerRadio.addEventListener('click', () => {
        signUpSubmitButton.textContent="SIGN UP";
    });

    /** validation */

    $('#signUpForm').submit(function (e) {
        serialized_array = $('#signUpForm').serializeArray();
        form_data = formToDict(serialized_array);

        if (validate(serialized_array, e)) {
            if (form_data.user == "employee") {
                e.preventDefault();

                /** redirect to aditional data panel */
                $('.basicAuth').css('display', 'none');
                $('#employeeAddAuth').css('display', 'block');
                $('#signUpEmployee').append(
                    "<input type='email' name='email' value='"+ form_data.email +"' style='display: none;'>" +
                    "<input type='password' name='password' value='"+ form_data.password +"' style='display: none;'>" +
                    "<input type='text' name='user' value='"+ form_data.user +"' style='display: none;'>"
                );
                error_close();
            }
        }
    });

    $('#signInForm').submit(function (e) {
        serialized_array = $('#signInForm').serializeArray();

        validate(serialized_array, e);
    });

    $('#yearPicker').mousewheel(function (e) {
        const MIN = 1900;
        const MAX = new Date().getFullYear();
        old_val = parseInt($('#yearPicker').val());
        new_val = old_val + e.deltaY;
        $('#yearPicker').val(
            (new_val >= MIN && new_val <= MAX) ? new_val : old_val
        );
    });

    $('#signUpEmployee').submit(function (e) {
        serialized_array = $('#signUpEmployee').serializeArray();

        validate(serialized_array, e);
    });

    $('#authBack').click(function(e) {
        $('.basicAuth').css('display', 'block');
        $('#employeeAddAuth').css('display', 'none');
        error_close();
    });
});
