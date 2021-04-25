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
            tax_return = data['tax']
        }
    })
    return tax_return
}



// Add current TAX value to the modal form input field
$(document).on('click', '.change-tax-btn', function () {
    var tax = get_tax()
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
    var valid = validateFormEmployee(data)
    
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

                    $('.modal-body-employee').html(''+
                    '<ul class="list-group">\
                    <li class="list-group-item">First Name: <b>'+data[0]+'</b></li>\
                    <li class="list-group-item">Second Name: <b>'+data[1]+'</b></li>\
                    <li class="list-group-item">Surname: <b>'+data[2]+'</b></li>\
                    <li class="list-group-item">Date Of Birth: <b>'+data[3]+'</b></li>\
                    <li class="list-group-item">Address: <b>'+data[4]+'</b></li>\
                    <li class="list-group-item">Tel.:<b>'+data[5]+'</b></li>\
                    <li class="list-group-item">Email: <b>'+data[6]+'</b></li>\
                    <li class="list-group-item">Position: <b>'+data[7]+'</b></li>\
                    <li class="list-group-item">Rate: <b>'+data[8]+'</b></li>\
                    <li class="list-group-item">Start Date: <b>'+data[9]+'</b></li>\
                    <li class="list-group-item">End Date: <b>'+data[10]+'</b></li>\
                    <li class="list-group-item">Is currently Employeed: <b>'+data[11]+'</b></li>\
                    <li class="list-group-item">National Insurance Number: <b>'+data[12]+'</b></li>\
                    <li class="list-group-item">Permission: <b>'+data[13]+'</b></li>\
                    <li class="list-group-item">PIN: <b>'+data[14]+'</b></li>\
                  </ul>'
                  )
                    $('.pin-exists-message').remove()
                   
                }
            }
        })
    }

})

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

// Get data from supplier registration form 
$(document).on('click', '#create_supplier_button', function(e){
    e.preventDefault();
    var data = []
    var valid_form = validateFormSupplier(data)
    if(valid_form){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            beforeSend: function (xhr) {

                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            url: CREATE_SUPPLIER,
            data: {
                'data': data
            },
            success: function (d) {
                $('.validation_message').html('')
                if(d['status'] == "Supplier with this name already exists"){
                    $('.validation_message').append('<small id="nameSupplierHelp" class="supplier-exists-message" style="color: red !important;">This supplier already exists!</small>')
                    $('#supplier_name_input').css('border-color', 'red')
                }
                else{
                    $('.hidden-reset-supplier').click()
                    $('#supplier-creation-modal').modal('show')

                    $('.modal-body-supplier').html(''+
                    '<ul class="list-group">\
                    <li class="list-group-item">Supplier Name: <b>'+data[0]+'</b></li>\
                    <li class="list-group-item">Email: <b>'+data[1]+'</b></li>\
                    <li class="list-group-item">Tel.: <b>'+data[2]+'</b></li>\
                    <li class="list-group-item">Lead Time: <b>'+data[3]+'</b></li>\
                  </ul>'
                  )
                    $('.pin-exists-message').remove()

                }
            }
        })
    }
})

function validateFormSupplier(data){

    var valid = true

    var supplier_name = $('#supplier_name_input').val()
    var email         = $('#supplier_email_input').val()
    var phone_number  = $('#supplier_number_input').val()
    var lead_time     = $('#supplier_lead_time_input').val()

    data.push(supplier_name)
    data.push(email)
    data.push(phone_number)
    data.push(lead_time)

    if(supplier_name == ""){
        $('#supplier_name_input').css('border-color', 'red')
        valid = false;
    }
    else $('#supplier_name_input').css('border-color', '#CFD4DA')

    if(email == ""){
        $('#supplier_email_input').css('border-color', 'red')
        valid = false;
    }
    else $('#supplier_email_input').css('border-color', '#CFD4DA')

    if(phone_number == ""){
        $('#supplier_number_input').css('border-color', 'red')
        valid = false;
    }
    else $('#supplier_number_input').css('border-color', '#CFD4DA')

    if(lead_time == ""){
        $('#supplier_lead_time_input').css('border-color', 'red')
        valid = false;
    }
    else $('#supplier_lead_time_input').css('border-color', '#CFD4DA')

    return valid
}

$(document).on('click', '.automatic-ordering-settings-btn', function(){
    $.ajax({
        method: "GET",
        url: AUTOMATED_ORDERING_SETTINGS,
        success: function (data) {
           
            var enable = data['enable']
            var email_confirmation = data['email_confirmation']
            var record_orders = data['record_orders']
            var email_text = data['email_text']

            if(enable){
                $('#enabled').prop('checked', true)
                
            }
            else{
                $('#enabled').prop('checked', false)
            }
            if(email_confirmation){
                $('#email-confirmation').prop('checked', true)
            }
            else{
                $('#email-confirmation').prop('checked', false)
            }
            if(record_orders){
                $('#record-orders').prop('checked', true)
            }
            else{
                $('#record-orders').prop('checked', false)
            }
            $('#email-text').val(email_text)

        }
    })
})

$(document).on('click', '#update-automated-ordering-settings', function(){
    var enable = $('#enabled').prop('checked')
    var email_confirmation =$('#email-confirmation').prop('checked')
    var record_orders = $('#record-orders').prop('checked')
    var email_text = $('#email-text').val()

    AUTOMATED_ORDERING_UPDATE_SETTINGS
    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data:{
            'enable':enable,
            'email_confirmation': email_confirmation,
            'record_orders':record_orders,
            'email_text':email_text
        },
        url: AUTOMATED_ORDERING_UPDATE_SETTINGS,
        success: function (data) {

            $('#automated-ordering-modal').modal('toggle')
        }
    })

})
