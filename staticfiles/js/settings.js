// On ready doc call a function that appends TAX value to HTML
$(function () {
    render_tax()
})
// Append argument to settings page tax value
function render_tax(tax = get_tax()) {
    tax = tax_representation(tax)
    $('.current-tax').text(tax + "%")
}

// Get TAX value from backend
function get_tax() {
    var tax_return = ""
    $.ajax({
        method: 'GET',
        url: GET_TAX,
        async: false,
        success: function (data) {
            // console.log(data['tax'])
            tax_return = data['tax']
        }
    })
    return tax_return
}



// Add current TAX value to the modal form input field
$(document).on('click', '.change-tax-btn', function () {
    var tax = get_tax()
    // console.log(tax)
    // console.log(tax.length)

    tax = tax_representation(tax)

    $('#tax-percentage-input').val(tax)
})
// Add to setting page changed tax value and save to backend
$(document).on('click', '#modal-tax-change-button', function () {
    var tax = $('#tax-percentage-input').val()
    render_tax(tax)
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: CHANGE_TAX.replace(0, (tax)),
        success: function (data) {
            // console.log(data)
        }
    })
})

$(document).on('click', '#modal-tax-change-button', function (e) {
    e.preventDefault();
    var new_tax = $('#tax-percentage-input').val()
    $('.current-tax').html(new_tax + "%")
    $('#tax-change').modal('toggle')
})


// If there are 2 0's in the last decimal places tax is represented as whole number
// otherwise, it is rendered as a decimal with 2 decimal places
function tax_representation(tax) {
    if (tax.length == 4) {
        if (tax.substring(2, tax.length) == "00")
            tax = tax.substring(0, 1)
    } else if (tax.length == 5) {
        if (tax.substring(3, tax.length) == "00")
            tax = tax.substring(0, 2)
    } else if (tax.length == 6) {
        if (tax.substring(4, tax.length) == "00")
            tax = tax.substring(0, 3)
    }
    return tax
}

// Creates an Employee 
$(document).on('click', '#create_employee_button', function (e) {
    e.preventDefault();
    data = []
    var valid = validateForm(data)
    // console.log(data)
    if (valid) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            beforeSend: function (xhr) {

                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            url: CREATE_EMPLOYEE,
            data: {
                'data': data
            },
            success: function (d) {
                $('.pin-exists-message').remove()
                if (d['status'] == "User with this pin exists") {
                    $('#pin_input').css('border-color', 'red')
                    $('.pin-row').append('<small id="pinUserHelp" class="pin-exists-message" style="color: red !important;">User with this pin exists</small>')
                }
                else {
                    $('.hidden-reset').click()
                    $('#employee-creation').modal('show')

                    $('.modal-body').html(''+
                    '<ul class="list-group">\
                    <li class="list-group-item">'+data[0]+'</li>\
                    <li class="list-group-item">'+data[1]+'</li>\
                    <li class="list-group-item">'+data[2]+'</li>\
                    <li class="list-group-item">'+data[3]+'</li>\
                    <li class="list-group-item">'+data[4]+'</li>\
                    <li class="list-group-item">'+data[5]+'</li>\
                    <li class="list-group-item">'+data[6]+'</li>\
                    <li class="list-group-item">'+data[7]+'</li>\
                    <li class="list-group-item">'+data[8]+'</li>\
                    <li class="list-group-item">'+data[9]+'</li>\
                    <li class="list-group-item">'+data[10]+'</li>\
                    <li class="list-group-item">'+data[11]+'</li>\
                    <li class="list-group-item">'+data[12]+'</li>\
                    <li class="list-group-item">'+data[13]+'</li>\
                    <li class="list-group-item">'+data[14]+'</li>\
                  </ul>'
                  )
                    $('.pin-exists-message').remove()
                   
                }
            }
        })
    }

})

function validateForm(data) {

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