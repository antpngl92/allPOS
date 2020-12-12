$('#clock_in_out').on('click', function (e) {
    e.preventDefault();


    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var pin = $('#pin').val()
    if (pin == "") {
        console.log("")
        $('#clock').css('color', 'red')
        $('#clock').html("You cannot clock in/out without a pin")
        
    }
    $.ajax({
        method: "POST",
        url: CLOCK_API,
        data: { 'pin': pin },
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (data) {

            $('#clock').css('color', 'white')
            $('#clock').html(data['status'])

        }
    })

})