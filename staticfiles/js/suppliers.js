$(document).on('click', '.update-supplier', function () {

    var supplier_pk = $(this).attr('data-id')
    var row_data = $('#' + supplier_pk).children()

    var name = $(row_data[0]).text()
    var email = $(row_data[1]).text()
    var phone = $(row_data[2]).text()
    var time = $(row_data[3]).text()

    $('#supplier-name').val(name)
    $('#supplier-email').val(email)
    $('#supplier-phone').val(phone)
    $('#supplier-time').val(time)

    $('#supplierModalLabel').html(supplier_pk + '# -- ' + name)

    $('#update-supplier-btn').attr('data-id', supplier_pk)
})

$(document).on('click', '#update-supplier-btn', function () {

    var supplier_pk = $(this).attr('data-id')

    var name = $('#supplier-name').val()
    var email = $('#supplier-email').val()
    var phone = $('#supplier-phone').val()
    var time = $('#supplier-time').val()

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data: {
            'name': name,
            'email': email,
            'phone': phone,
            'time': time
        },
        url: UPDATE_SUPPLIER.replace("0", supplier_pk),
        success: function (data) {
            var row_data = $('#' + supplier_pk).children()

            $(row_data[0]).text(name)
            $(row_data[1]).text(email)
            $(row_data[2]).text(phone)
            $(row_data[3]).text(time)

            $('#supplier-modal').modal('toggle')
        }
    })

})


$(document).on('click', '.btn-delete-supplier', function(){
    var supplier_pk = $(this).attr('data-id')
    $(this).parent().parent().remove()
    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        url: DELETE_SUPPLIER.replace("0", supplier_pk),
        success: function (data) {
            
        }
    })

})













