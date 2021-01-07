$(document).ready(function() {
    $('.nav-item').removeClass('active')
    $('#browser').addClass('active')

    storageoffers = sessionStorage.getItem("jobOffers")
    if(storageoffers != null) {
        displayJobList(storageoffers);
    }

    $('#searchBtn').click(function() {

        var jqxhr = $.ajax({
            method: "GET",
            url: "/recommendation/employee",
            data: {
                "keywords": $('#searchInput').val()
            },
            timeout: 0,
            beforeSend: function() {
                error_close();
                loader_start();
            }
        })
        .done(function(response) {
            displayJobList(response);
            sessionStorage.setItem("jobOffers", response);
        })
        .fail(function(response) {
            error_show("Something went wrong!")
        })
        .always(function() {
            loader_stop();
        });

    });
})


function displayJobList(jobs) {
    if (jobs !== "") {
        $('#startMsg').remove();
        $('#announcements').html(
            jobs
        )
        $('.rateJob').click(function(e) {
            var data = e.target.id.split('_');
            var rate_val = data[0] == "like" ? 1 : 0;
            var job_id = parseInt(data[1]);
            rate(rate_val, job_id);
        });
    }
    else {
        error_show("Nothing to display, try to use correct spelling and clarify yout interests, experiences or keywords!");
    }
}

function rate(rate_val, job_id) {
    var jqxhr = $.ajax({
        method: "POST",
        url: "/user/employee/rating",
        data: {
            "rate": rate_val,
            "job_id": job_id,
        },
        timeout: 0
    })
    .done(function(response) {
        error_show("Thank you for rating!");
        if (rate_val == 1) {
            $('#like_'+job_id).parent( ".ldl" ).addClass('ratactive')
            $('#dnlike_'+job_id).parent( ".ldl" ).removeClass('ratactive')
        }
        else {
            $('#like_'+job_id).parent( ".ldl" ).removeClass('ratactive')
            $('#dnlike_'+job_id).parent( ".ldl" ).addClass('ratactive')
        }


        sessionStorage.setItem(
            "jobOffers", 
            $('#announcements').html()
        );
    })
    .fail(function(response) {
        error_show("Something went wrong!")
    })
}
