
function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    // Return array of year and week number
    return [d.getUTCFullYear(), weekNo];
}
var result = getWeekNumber(new Date());

var week_str = String(result[0] + "-W" + ('0' + result[1]).slice(-2))

$(document).on('click', '.get_weekly_schedule', function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var week_number = $('#week_input').val()
    week_number = week_number.substring(6, 8)

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        dataType: 'json',
        url: GET_WEEKLY_SCHEDULE,
        data: {
            'data': week_number
        },
        success: function (d) {
            console.log(d)
            $('.view-edit-schedule').html('')
            $('.table-body').html('')
            for (var i = 0; i < d['schedules'].length; i++) {

                $('.table-body').append(`
               <tr>
                    <td>`+ d['schedules'][i][1] + `</td>
                    <td>`+ d['schedules'][i][2] + `</td>
                    <td>`+ d['schedules'][i][3].slice(0, 5) + `</td>
                    <td>`+ d['schedules'][i][4].slice(0, 5) + `</td>
                    <td class="shedule_buttons">
                        <button type='button' data-row="`+ (i + 1) + `" data-employee="` + d['schedules'][i][5] + `" class='btn btn-info schedule-button' id="` + d['schedules'][i][0] + `">Update</button>
                    </td>
                    <td class="shedule_buttons">
                    <button type='button' data-row="`+ (i + 1) + `" class='btn btn-info delete-schedule-button' data-id="` + d['schedules'][i][0] + `">Delete</button>
                    </td>
                </tr>
               `)
            }

        }
    })

})
$(document).on('click', '.close-data', function () {
    $('.view-edit-schedule').html('')
})

$(document).on('click', '.schedule-button', function () {
    var schedule_id = $(this).attr('id')
    var employee_id = $(this).data('employee')
    var row_num = $(this).data('row')

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        dataType: 'json',
        url: GET_SCHEDULE.replace('0', schedule_id),
        success: function (d) {


            var rendering_data = '' +
                `<form class="needs-validation mt-5 ml-5" style="margin-top: 75px !important; width: 60%;" novalidate> <p hidden>{% csrf_token %}<p>
                <div class="form-group row">\
                    <label for="scheduled_employee_input" class="col-2 col-form-label">Scheduled Employee</label>
                    <div class="col-10">
                        <select class="form-control select-employee" id="sel1">

                        </select>

                    </div>
                </div>

            <div class="form-group row">
                <label for="shift_date_input" class="col-2 col-form-label">Shift Date</label>
                <div class="col-10">
                    <input class="form-control" type="date" id="shift_date_input" value="` + d['schedules'][0][2] + `" placeholder="Shift Date" required>
                </div>
            </div>

            <div class="form-group row">
                <label for="shift_start_input" class="col-2 col-form-label">Shift Starts</label>
                <div class="col-10">
                    <input class="form-control" type="time" id="shift_start_input" value="` + d['schedules'][0][3] + `" placeholder="Shift Start">
                </div>
            </div>

            <div class="form-group row">
                <label for="shift_end_input" class="col-2 col-form-label">Shift Ends</label>
                <div class="col-10">
                    <input class="form-control" type="time" id="shift_end_input" value="` + d['schedules'][0][4] + `" placeholder="Shift End">
                </div>
            </div>
            
            <div class="text-center">
                <button type="submit" id="update_schedule_button" data-row="` + row_num + `" data-employee="` + d['schedules'][0][5] + `" data-id="` + d['schedules'][0][0] + `" class="btn btn-info">Update Schedule</button>
                <button type="button" class="btn btn-info close-data">Close</button>
            </div>
            <input type="reset" class="hidden-reset" value="Reset" hidden/>
        </form>`



            $('.view-edit-schedule').html('')
            $('#sel1').html('')
            $('.view-edit-schedule').append(rendering_data)

            for (var i = 0; i < d['employees'].length; i++) {
                if (employee_id == d['employees'][i][0])
                    $('#sel1').append("<option selected value=" + d['employees'][i][0] + ">" + d['employees'][i][1] + " " + d['employees'][i][2] + "</option>")

                $('#sel1').append("<option value=" + d['employees'][i][0] + ">" + d['employees'][i][1] + " " + d['employees'][i][2] + " </option>")

            }
        }
    })
})

$(document).on('click', '#update_schedule_button', function (e) {
    e.preventDefault();

    var schedule_id = $(this).data('id')
    var selected_employee_id = $('.select-employee option:selected').attr('value')
    var selected_employee_name = $('.select-employee option:selected').html()
    var shift_date = $('#shift_date_input').val()
    var shift_start = $('#shift_start_input').val()
    var shift_end = $('#shift_end_input').val()
    var row_num = $(this).data('row')

    data = []
    data.push(schedule_id)
    data.push(selected_employee_id)
    data.push(shift_date)
    data.push(shift_start)
    data.push(shift_end)


    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        dataType: 'json',
        data: {
            'data[]': data,
        },
        url: UPDATE_SCHEDULE.replace('0', schedule_id),
        success: function (d) {
            var table_row = $('*[data-row="' + row_num + '"]').parent().parent()

            $(table_row).html(`
           <td>`+ selected_employee_name + `</td>
           <td>`+ shift_date + `</td>
           <td>`+ shift_start.slice(0, 5) + `</td>
           <td>`+ shift_end.slice(0, 5) + `</td>
           <td class="shedule_buttons">
               <button type='button' data-row="`+ row_num + `" data-employee="` + selected_employee_id + `" class='btn btn-info schedule-button' id="` + schedule_id + `">Update</button>
           </td>
           <td class="shedule_buttons">
           <button type='button' data-row="`+ row_num + `" class='btn btn-info delete-schedule-button' data-id="` + schedule_id + `">Delete</button>
           </td>
           `)

            $('.view-edit-schedule').html('')
        }
    })

})

$(document).on('click', '.create_schedule', function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    var rendering_data = `<form class="needs-validation mt-5 ml-5" style="margin-top: 75px !important; width: 60%;" novalidate> <p hidden>{% csrf_token %}<p>
    <div class="form-group row">\
        <label for="scheduled_employee_input" class="col-2 col-form-label">Scheduled Employee</label>
        <div class="col-10">
            <select class="form-control select-employee" id="sel1" required>

            </select>

        </div>
    </div>

    <div class="form-group row">
        <label for="shift_date_input" class="col-2 col-form-label">Shift Date</label>
        <div class="col-10">
            <input class="form-control" type="date" id="shift_date_input" placeholder="Shift Date" required>
        </div>
    </div>

    <div class="form-group row">
        <label for="shift_start_input" class="col-2 col-form-label">Shift Starts</label>
        <div class="col-10">
            <input class="form-control" type="time" id="shift_start_input" placeholder="Shift Start" required>
        </div>
    </div>

    <div class="form-group row">
        <label for="shift_end_input" class="col-2 col-form-label">Shift Ends</label>
        <div class="col-10">
            <input class="form-control" type="time" id="shift_end_input" placeholder="Shift End" required>
        </div>
    </div>

    <div class="text-center">
        <button type="submit" id="create_schedule_button" class="btn btn-info">Create Schedule</button>
        <button type="button" class="btn btn-info close-data">Close</button>
    </div>
    <input type="reset" class="hidden-reset" value="Reset" hidden/>
    </form>`


    $('.view-edit-schedule').append(rendering_data)

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_ALL_EMPLOYEES,
        success: function (d) {

           for (var i = 0; i < d.length; i++) {
                $('#sel1').append("<option value=" + d[i][0] + ">" + d[i][1] + " " + d[i][2] + " </option>")
            }
        }
    })
})

$(document).on('click', '#create_schedule_button', function(){
    var selected_employee_id = $('.select-employee option:selected').attr('value')
    var selected_employee_name = $('.select-employee option:selected').html()
    var shift_date = $('#shift_date_input').val()
    var shift_start = $('#shift_start_input').val()
    var shift_end = $('#shift_end_input').val()

    data = []
    data.push(selected_employee_id)
    data.push(shift_date)
    data.push(shift_start)
    data.push(shift_end)


    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        dataType: 'json',
        data: {
            'data[]': data,
        },
        url: CREATE_SCHEDULE,
        success: function (d) {
            if(d['status'] == "Success")
            location.reload();
        }
    })
})

$(document).on('click','.delete-schedule-button', function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var schedule_id = $(this).data('id')

    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url:DELETE_SCHEDULE.replace("0", schedule_id),
        success: function(d){
            
        }
    })
    $(this).parent().parent().remove()
})

const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            current_week: week_str
        }
    },

})

const mountedApp = app.mount('#app')



