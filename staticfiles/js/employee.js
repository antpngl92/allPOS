// View Employee info
$(document).on("click", '.employee_info', function () {
    var employee_id = $(this).data('id')
    data = get_employee_data(employee_id)

    var second_name = '<li class="list-group-item">Second Name: <span class="font-weight-bold">' + data.second_name + '</span></li>'
    var employed = "Yes"
    var end_date = '<li class="list-group-item">Termination of Employment: <span class="font-weight-bold">' + data.end_date + '</span></li>'
    if (data.second_name == "") {
        second_name = ""
    }
    if (data.is_employeed == false) {
        employed = "No"
    }
    if (data.end_date == null) {
        end_date = ""
    }

    var rendering_data = '' +
        '<ul class="list-group emlpoyee-details">\
            <li class="list-group-item">First Name:                <span class="font-weight-bold">'+ data.first_name + '</span></li>\
            '+ second_name + '\
            <li class="list-group-item">Last Name:                 <span class="font-weight-bold">'+ data.last_name + '</span></li>\
            <li class="list-group-item">Date Of Birth:             <span class="font-weight-bold">'+ data.date_of_birth + '</span></li>\
            <li class="list-group-item">Address:                   <span class="font-weight-bold">'+ data.address + '</span></li>\
            <li class="list-group-item">Tel. Number:               <span class="font-weight-bold">'+ data.tel_number + '</span></li>\
            <li class="list-group-item">Email:                     <span class="font-weight-bold">'+ data.email + '</span></li>\
            <li class="list-group-item">Position:                  <span class="font-weight-bold">'+ data.position + '</span></li>\
            <li class="list-group-item">Wage Rate:                 <span class="font-weight-bold">£'+ data.hourly_pay_rate + ' p/h</span></li>\
            <li class="list-group-item">Still Employed:            <span class="font-weight-bold">'+ employed + '</span></li>\
            <li class="list-group-item">Employed ON:            <span class="font-weight-bold">'+ data.start_date + '</span></li>\
            '+ end_date + '\
            <li class="list-group-item">National Insurance Number: <span class="font-weight-bold">'+ data.nin + '</span></li>\
            <li class="list-group-item">Permission Level:          <span class="font-weight-bold">'+ data.permission_level + '</span></li>\
            <li class="list-group-item">Pin:                       <span class="font-weight-bold">'+ data.pin + '</span></li>\
        </ul>\
        <div class="text-center" style="margin-top: 30px;"><button type="button" class="btn btn-info close-data">Close</button></div>'

    add_data_to_component('.view-edit-employee', rendering_data)
})

// Delete Employee
$(document).on('click', '.employee_delete', function () {
    var employee_id = $(this).data('id');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: DELETE_EMPLOYEE.replace("0", employee_id),
        success: function (data) {
            empty_component('.view-edit-employee')
            $('#' + employee_id).remove()
        }

    })

})

// Update Employee Details
$(document).on('click', '.employee_update', function () {
    var id = $(this).data('id')
    var data = get_employee_data(id)

    var is_employeed = `<input class="form-control" type="checkbox" id="is_employeed_input"></input>`
    if(data.is_employeed == true) is_employeed = `<input class="form-control" type="checkbox" id="is_employeed_input" checked></input>`

    var rendering_data = '' +
        `<form class="needs-validation" novalidate> <p hidden>{% csrf_token %}<p>
            <div class="form-group row">\
                <label for="first_name_input" class="col-2 col-form-label">Name</label>
                <div class="col-10">
                    <input class="form-control" type="text" id="first_name_input" value="` + data.first_name + `" placeholder="Enter First Name">
                </div>
            </div>

            <div class="form-group row">
                <label for="middle_name_input" class="col-2 col-form-label">Middle</label>
                <div class="col-10">
                    <input class="form-control" type="text" id="middle_name_input" value="` + data.second_name + `" placeholder="Enter Middle Name">
                </div>
            </div>


            <div class="form-group row">
                <label for="surname_input" class="col-2 col-form-label">Surname</label>
                <div class="col-10">
                    <input class="form-control" type="text" id="surname_input" value="` + data.last_name + `" placeholder="Enter Surname">
                </div>
            </div>
        <div class="form-group row">
            <label for="date_of_birth_input" class="col-2 col-form-label">DOB</label>
            <div class="col-10">
                <input class="form-control" type="date" id="date_of_birth_input" value="` + data.date_of_birth + `" placeholder="Enter Date Of Birth" required>
                <div class="invalid-feedback">
                Please choose a username.
                </div>
            </div>
        </div>
        <div class="form-group row">
            <label for="address_input" class="col-2 col-form-label">Address</label>
            <div class="col-10">
                <input class="form-control" type="text" id="address_input" value="` + data.address + `" placeholder="Enter Address">
            </div>
        </div>
        <div class="form-group row">
            <label for="contact_num_input" class="col-2 col-form-label">Tel.</label>
            <div class="col-10">
                <input class="form-control" type="text" id="contact_num_input" value="` + data.tel_number + `" placeholder="Enter Contact Number">
            </div>
        </div>
        <div class="form-group row">
            <label for="email_input" class="col-2 col-form-label">Email</label>
            <div class="col-10">
                <input class="form-control" type="email" id="email_input" value="` + data.email + `" placeholder="Enter Email">
            </div>
        </div>
        <div class="form-group row">
            <label for="position_input" class="col-2 col-form-label">Position</label>
            <div class="col-10">
                <input class="form-control" type="text" id="position_input" value="` + data.position + `"  placeholder="Enter Employee's Position">
            </div>
        </div>
        <div class="form-group row">
        <label for="pay_rate_input" class="col-2 col-form-label">Rate</label>
            <div class="col-10">
                <input class="form-control" type="number" step="0.01" id="pay_rate_input" value="` + data.hourly_pay_rate + `"  placeholder="Enter Employee's Pay Rate">
            </div>
        </div>
        <div class="form-group row">
            <label for="start_date_input" class="col-2 col-form-label">Start</label>
            <div class="col-10">
                <input class="form-control" type="date" value="` + data.start_date + `"  id="start_date_input" required>
            </div>
        </div>
        <div class="form-group row">
            <label for="date" class="col-2 col-form-label">End</label>
            <div class="col-10">
                <input class="form-control" type="date"  value="` + data.end_date + `"   id="end_date_input">
            </div>
        </div>
        <div class="form-group row">
            <label for="is_employeed_input" class="col-2 col-form-label">Employeed</label>
            <div class="col-10">
                `+is_employeed+`
            </div>
        </div>
        <div class="form-group row">
            <label for="nin_input" class="col-2 col-form-label">NIN</label>
            <div class="col-10">
                <input class="form-control" type="text" id="nin_input"  value="` + data.nin + `" placeholder="Enter National Insurance Number">
            </div>
        </div>
        <div class="form-group row">
            <label for="permission_level_input" class="col-2 col-form-label">Permissions</label>
            <div class="col-10">
                <input class="form-control" type="number" min="1" max="3" step="1"  value="` + data.permission_level + `"  id="permission_level_input" placeholder="Enter Permission Level">
                <small id="emailHelp" class="form-text text-muted">1- Manager, 2-Supervisor, 3-Employee</small>
            </div>
        </div>
        <div class="form-group row pin-row">
            <label for="pin_input" class="col-2 col-form-label">PIN</label>
            <div class="col-10">
                <input class="form-control" type="number" step="1" id="pin_input"  value="` + data.pin + `" placeholder="Enter Pin">
            </div>
        </div>
        <div class="text-center">
            <button type="submit" id="update_employee_button" data-id="`+id+`" class="btn btn-info">Update Employee</button>
            <button type="button" class="btn btn-info close-data">Close</button>
        </div>
        <input type="reset" class="hidden-reset" value="Reset" hidden/>
    </form>`

    rendering_data
    add_data_to_component('.view-edit-employee', rendering_data)
})

$(document).on('click', '#update_employee_button', function(e){
    var id = $(this).data('id');
    e.preventDefault();
    data = []
    var valid_form = validateFormEmployee(data)
    if(valid_form){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "PUT",
            beforeSend: function (xhr) {

                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            content_type:'application/json',
            url: UPDATE_EMPLOYEE.replace("0", id),
            data: {
                'data': data
            },
            success: function (d) {
                 $('#'+id+' strong').html(data[0] + " " + data[1] + " " + data[2])
            }
        })
    }
})




$(document).on('click', '.close-data', function () {
    empty_component(".view-edit-employee")
})


function empty_component(component) {
    $(component).html("")
}

function add_data_to_component(component, data) {
    $(component).html(data)
    $(component).append('')
}

// Ajax for getting Employee data
function get_employee_data(id) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var employee_data = []

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_EMPLOYEE.replace("0", id),
        async: false,
        success: function (d) {
            var js_obj = JSON.parse(d)
            employee_data = js_obj[0]['fields']

        }
    })
    return employee_data
}

function validateFormEmployee(data) {

    valid = true

    var first_name = $('#first_name_input').val()
    var middle_name = $('#middle_name_input').val()
    var surname_name = $('#surname_input').val()
    var dob = $('#date_of_birth_input').val()
    var address = $('#address_input').val()
    var tel_number = $('#contact_num_input').val()
    var email = $('#email_input').val()
    var possition = $('#position_input').val()
    var pay_rate = $('#pay_rate_input').val()
    var start_date = $('#start_date_input').val()
    var end_date = $('#end_date_input').val()
    var is_employeed = $('#is_employeed_input').is(':checked')
    var nin = $('#nin_input').val()
    var permission = $('#permission_level_input').val()
    var pin = $('#pin_input').val()

    data.push(first_name)
    data.push(middle_name)
    data.push(surname_name)
    data.push(dob)
    data.push(address)
    data.push(tel_number)
    data.push(email)
    data.push(possition)
    data.push(pay_rate)
    data.push(start_date)
    data.push(end_date)
    data.push(is_employeed)
    data.push(nin)
    data.push(permission)
    data.push(pin)

    if (first_name == "") {
        $('#first_name_input').css('border-color', 'red')
        valid = false;
    }
    else $('#first_name_input').css('border-color', '#CFD4DA')

    if (surname_name == "") {
        $('#surname_input').css('border-color', 'red')
        valid = false;
    }
    else $('#surname_input').css('border-color', '#CFD4DA')

    if (dob == "") {
        $('#date_of_birth_input').css('border-color', 'red')
        valid = false;
    }
    else $('#date_of_birth_input').css('border-color', '#CFD4DA')

    if (email == "") {
        $('#email_input').css('border-color', 'red')
        valid = false;
    }
    else $('#email_input').css('border-color', '#CFD4DA')

    if (possition == "") {
        $('#position_input').css('border-color', 'red')
    }
    else $('#position_input').css('border-color', '#CFD4DA')

    if (pay_rate == "") {
        $('#pay_rate_input').css('border-color', 'red')
        valid = false;
    }
    else $('#pay_rate_input').css('border-color', '#CFD4DA')

    if (start_date == "") {
        $('#start_date_input').css('border-color', 'red')
        valid = false;
    }
    else $('#start_date_input').css('border-color', '#CFD4DA')

    if (nin == "") {
        $('#nin_input').css('border-color', 'red')
        valid = false;
    }
    else $('#nin_input').css('border-color', '#CFD4DA')

    if (permission == "") {
        $('#permission_level_input').css('border-color', 'red')
        valid = false;
    }
    else $('#permission_level_input').css('border-color', '#CFD4DA')

    if (pin == "") {
        $('#pin_input').css('border-color', 'red')
        valid = false;
    }
    else $('#pin_input').css('border-color', '#CFD4DA')

    return valid
}


