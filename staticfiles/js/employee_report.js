$(document).on('change', '#single_employee', function(){
    
    provided_input('.settings_employee')
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    addElement('.select_employee ')
    $.ajax({
        method: "GET",
        beforeSend: function (xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          },
        url: GET_EMPLOYEES,
        success: function(data){    
            $('#sel1').html("")       
            for (var i = 0; i < data.length; i++) {
                $('#sel1').append("<option value=" + data[i][0] + ">" + data[i][1] + " " + data[i][2] + " </option>")
            }
        }
    })
})

$(document).on('change', '#all_employees', function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    removeElement('.select_employee ')
    provided_input('.settings_employee')
    
})

$(document).on('change', '#single_day', function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    removeElement('.select_time_period_date')
    addElement('.select_specific_date')
    provided_input('.settings_date')
})

$(document).on('change', '#time_period', function(){
    removeElement('.select_specific_date')
    addElement('.select_time_period_date')
    provided_input('.settings_date')
})



// Generate Report Button on click
$(document).on('click', '.generate_report_button', function(){

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    var selected_employee_id = ""
    var date = ""
    var date_from = ""
    var date_to = ""

    if(!$('#single_employee').is(':checked') && !$('#all_employees').is(':checked')){
        missing_input('.settings_employee') 
    }
    else if($('#single_employee').is(':checked')){
        selected_employee_id = $('.select-employee option:selected').attr('value')
    }
    else{
        selected_employee_id = "all"
    }

    if(!$('#single_day').is(':checked') && !$('#time_period').is(':checked')){
        missing_input('.settings_date') 
    }
    else if($('#single_day').is(':checked')){
        date = $('#date_for_report').val()
    }
    else{
        date_from = $('#date_for_report_start').val()
        date_to = $('#date_for_report_end').val()
    }

    if(date_from > date_to){
        $('.invalid_date').removeClass('hidden-element')
    }
    else{
        $('.invalid_date').addClass('hidden-element')
    }


    $.ajax({
        method: "GET",
        beforeSend: function (xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          },
        data: {
            'employee' : selected_employee_id, 
            'date'     : date,
            'from'     : date_from,
            'to'       : date_to
            
        },
        url: GENERATE_REPORT,
        success: function(data){
            console.log(data)
            
        }
    })

})


function addElement(element){
    $(element).removeClass('hidden-element')
}
function removeElement(element){
    $(element).addClass('hidden-element')
}

function missing_input(element){
    $(element).addClass("missing_input")
    addElement(element + ' .text-muted')
}
function provided_input(element){
    $(element).removeClass("missing_input")
    removeElement(element + ' .text-muted')
}
