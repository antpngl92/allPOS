$(document).on('click','#modal-order-number-button', function(e){
    e.preventDefault();
    var input_val = $('#order-number-input').val()
    $('.order-number').html(input_val)
    $('.close').click()
})

$(document).on('click','#modal-order-type-button', function(e){
    e.preventDefault();
    var order_type  = $('input[type=radio][name=order-type]:checked').val()
    $('.order-type').html(order_type)  
    $(order_type).prop('checked', false)
    $('.close').click()
    keep_track_of_total_price()
})
