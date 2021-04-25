$(document).on('click', '.send-butt', function(){

    var order_num = $('.order-number').html()
    $('#sendOrderModelLabel').html('')


    var num_orders = $('.order-product-list-table-body').children()

    if(num_orders.length == 0){
        
        $('.modal-body-sending-status').html(`
            No products selected!
        `)
    }
    else{
        $('#sendOrderModelLabel').html('Sending order: ' + order_num)
        $('.modal-body-sending-status').html(`
        Order number `+order_num+`  sent!
    `)
    }
})