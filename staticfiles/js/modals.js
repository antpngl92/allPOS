$('#modal-order-number-button').on('click', function(e){
    e.preventDefault();
    var input_val = $('#order-number-input').val()
    $('.order-number').html(input_val)
    $('.close').click()
})