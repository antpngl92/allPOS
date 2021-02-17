$(function () {
    var date = new Date();


    // Set the month and year required
    // Default current month and year
    var year = date.getFullYear();
    var month = date.getMonth()

    set_calendar_month_year(month, year, '.month1', '.year')

    // Get an array with all the days of the week required
    // Default current week
    let week = set_week_days(date)


    // Get the list elements of the calendar from the DOM 
    // and for each element apped the date corresponding to each week day
    var list_dates = $('.days-of-the-month')
    for (var i = 0; i < list_dates.length - 1; i++) {
        var week_day = week[i]
        $(list_dates[i + 1]).html(week_day.slice(8, 10))
    }


    //Get all employees schedule and render it 
    get_employees_schedule(week)

    // Populate each Employee row colums 
    // with Employee's schedule for the week
    var employee_rows = $('.employees ')
    for (var i = 0; i < employee_rows.length; i++) {
        var temp_row = employee_rows[i]
        for (var j = 1; j < $(temp_row).children().length; j++) {
            var children_of_ul = $(temp_row).children()[j]
            $(children_of_ul).attr('class', week[j - 1].slice(8, 10))
        }
    }
})


// Append the week days to an array 
// And return the array with the month days for this week
function set_week_days(data_obj) {
    var week_arr = []
    for (let i = 1; i <= 7; i++) {
        let first = data_obj.getDate() - data_obj.getDay() + i
        let day = new Date(data_obj.setDate(first)).toISOString()
        week_arr.push(day)
    }
    return week_arr
}

// Set Month and Year given month number, year, DOM month component and DOM year component
function set_calendar_month_year(month_number, year, month_component, year_component) {
    months = {
        0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July",
        7: "August", 8: "September", 9: "October", 10: "November", 11: "December",
    }

    $(month_component).text(months[month_number])
    $(year_component).text(year)
}


function get_employees_schedule(week) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        data: {
            'week[]': week,
        },
        url: GET_SCHEDULE_FOR_ROTA,
        success: function (data) {
            console.log(data[0])
            for (var i = 0; i < data.length; i++) {
                var employee = data[i]['employee_id']
                var date = data[i]['work_date'].toString()
                date = date.slice(8)
                var employee_ul = $('#' + employee).children()
                // console.log(employee_ul)
                for (var j = 1; j < employee_ul.length; j++) {
                    if ($(employee_ul[j]).attr('class') == date) {
                        $(employee_ul[j]).css('color', '#133B66')
                        $(employee_ul[j]).html(data[i]['start_work_hour'].slice(0, 5) + " - " + data[i]['end_work_hour'].slice(0, 5))
                    }
                }
            }
        }
    })

}
