var colors = ["#5AA8E5", "#7786D1", "#9A73D2", "#C261CA", "#DD75BC", "#DC5970", "#E4884F", "#F8D95F", "#95DB5D", "#5FA6B7"];

// Import PIE Chart
$(function () {
    //Changes the colors of the top 10 list numbers
    var items = $('.quantity-sold')
    for (var i = 0; i < items.length; i++) {
        items[i].style.color = colors[i];
    }
    // Get the product names and sold quantity 
    var items_temp = $('.product-name')
    var number_temp = $('.quantity-sold')
    var items = []
    var numbers = []
    // Insert the product names and sold quantity into lists
    for (var i = 0; i < items_temp.length; i++) {
        items[i] = items_temp[i].innerText
        numbers[i] = number_temp[i].innerText
    }
    // Integrate products names and sold quantity into pie chart
    var ctxP = document.getElementById("pieChart").getContext('2d');
    var myPieChart = new Chart(ctxP, {
        type: 'doughnut',
        data: {
            labels: items,
            datasets: [{
                data: numbers,
                backgroundColor: colors,
                hoverBackgroundColor: ["#9dc3e0", "#a3aac9", "#b19dcf", "#c69bc9", "#d9a5c8", "#cf97a1", "#d6a98d", "#faeebe", "#b3d498", "#b1c3c7"]
            },
            ]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            tooltip: {
                enable: false
            },
        }
    });
})


// Import BAR Chart
$(function () {
    // Get data from back-end 
    var this_week_daily_revenue = JSON.parse($('#hidden').text());
    var last_week_daily_revenue = JSON.parse($('#hidden2').text());
    var weeek_days_list = JSON.parse($('#hidden3').text());
    var this_weeks_color_background = 'rgba(157, 195, 224, 1)'
    var this_weeks_color_border = 'rgba(90, 168, 229, 1)'
    var last_weeks_color_background = 'rgba(198, 155, 201, 1)'
    var last_weeks_color_border = 'rgba(194, 97, 202, 1)'
    // Integrate the data into the barchart
    var ctx = document.getElementById("barChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: weeek_days_list,
            datasets: [{
                label: 'This Week',
                data: this_week_daily_revenue,
                backgroundColor: [
                    this_weeks_color_background,
                    this_weeks_color_background,
                    this_weeks_color_background,
                    this_weeks_color_background,
                    this_weeks_color_background,
                    this_weeks_color_background,
                    this_weeks_color_background,
                ],
                borderColor: [
                    this_weeks_color_border,
                    this_weeks_color_border,
                    this_weeks_color_border,
                    this_weeks_color_border,
                    this_weeks_color_border,
                    this_weeks_color_border,
                    this_weeks_color_border,
                ],
                borderWidth: 2
            }, {
                label: 'Last Week',
                data: last_week_daily_revenue,
                backgroundColor: [
                    last_weeks_color_background,
                    last_weeks_color_background,
                    last_weeks_color_background,
                    last_weeks_color_background,
                    last_weeks_color_background,
                    last_weeks_color_background,
                    last_weeks_color_background,

                ],
                borderColor: [
                    last_weeks_color_border,
                    last_weeks_color_border,
                    last_weeks_color_border,
                    last_weeks_color_border,
                    last_weeks_color_border,
                    last_weeks_color_border,
                    last_weeks_color_border,

                ],
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                legend: {
                    display: true
                },
                tooltip: {
                    enable: true
                },
            }
        }
    });
})

$(function () {
    // Create a new order - redirect to EPOS screen
    $('.first-row-button2').on('click', function () {
        location.replace("/")
    })
    // List Orders
    $('.first-row-button1').on('click', function () {
        $('.analytics-order-list-modal-body').html('')
        $('#orders-modal-label').html('Orders/')
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        get_orders(csrftoken)

    })
})
$(function () {
    $('.table-row-list').on('click-row.bs.table', function () {
    })
})
// Get the list of all orders
function get_orders(csrftoken) {
    $('.analytics-order-list-modal-body').html('')
    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: ORDERS_END_POINT,
        success: function (data) {

            $('.analytics-order-list-modal-body').append('' +
                    '   <table class="table orders-list-analytics">\
                        <thead>\
                            <tr class="table-row-orders">\
                                <th scope="col">ID</th>\
                                <th scope="col">Date</th>\
                                <th scope="col">Time</th>\
                                <th scope="col">Number</th>\
                                <th scope="col">Total</th>\
                                <th scope="col">Type</th>\
                                <th scope="col">Paid</th>\
                                <th scope="col">View Order</th>\
                            </tr>\
                        </thead>\
                        <tbody>\
                        </tbody>\
                    </table>')

            
            for (var i = data.length - 1; i >= 0; i--) {
                var type = data[i]['order_type']
                var curr_type = "Have In"

                var paid = data[i]['paid']
                var curr_paid = "Paid"

                if (paid == false) curr_paid = "On Hold"
                if (type == 1) curr_type = "Take Out"
                
                
                $('.orders-list-analytics tbody').append('' +
                    '<tr class="table-row-list" id=' + data[i]['id'] + '>\
                        <td scope="row" style="font-weight:bold";>'+ data[i]['id'] + '</td>\
                        <td>'+ data[i]['date'] + '</td>\
                        <td>'+ data[i]['time'].substring(0, 8) + '</td>\
                        <td>'+ data[i]['order_numer'] + '</td>\
                        <td>£'+ data[i]['total_amount'] + '</td>\
                        <td>'+ curr_type + '</td>\
                        <td>'+ curr_paid + '</td>\
                        <td><a href="#" id='+ data[i]['id'] + ' class="btn btn-light view-specific-order">View</a></td>\
                    </tr>')
            }
        }
    })
}

// Modal Header Breadcrumb
$(document).on('click', '.back_to_orders', function () {
    $('#orders-modal-label').html('Orders/')
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    get_orders(csrftoken)
})
// View a specific order from the order list
$(document).on('click', '.view-specific-order', function () {
    var order_id = $(this).attr('id')
    $('.analytics-order-list-modal-body').html('') // When order details are set-up for rendering DELETE this!
    var modal_text = $('#orders-modal-label').html()
    $('#orders-modal-label').html('<a href="#" class="back_to_orders">' + modal_text + '</a>Order: ' + order_id)
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    get_specific_order(csrftoken, order_id)

})

function get_specific_order(csrftoken, order_id) {
    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: ORDER_END_POINT.replace('0', order_id),
        success: function (data) {
            $('.analytics-order-list-modal-body').append('' +
                '<table class="table specific-order-products">\
                    <thead>\
                        <tr>\
                            <th scope="col">Product</th>\
                            <th scope="col">Quantity</th>\
                            <th scope="col">Retail Price</th>\
                            <th scope="col">Total Price</th>\
                            </tr>\
                    </thead>\
                    <tbody>\
                    </tbody>\
                    </table>\
            ')
            var total = 0
            for(var i = 0; i < data['q'].length;i++){
                $('.specific-order-products tbody').append(''+
                '<tr>\
                    <td scope="row">'+data['p'][i] + '</td>\
                    <td>'+data['q'][i] + '</td>\
                    <td>£'+data['rp'][i] + '</td>\
                    <td>£'+ (data['rp'][i] * data['q'][i]).toFixed(2) +'</td>\
                </tr>\
                ')
                total = total + (data['rp'][i] * data['q'][i])
            }
            $('.specific-order-products tbody').append(''+
            '<tr>\
                <td scope="row"><b>Order Total: </b></td>\
                <td></td>\
                <td></td>\
                <td>£'+total.toFixed(2)+'</td>\
            </tr>\
            ')
        }
    })
}

