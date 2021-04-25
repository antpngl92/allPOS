$(document).on('click', '.update-product', function () {
    var product_pk = $(this).attr('data-id')
    $('#product-category').html('')
    $('.product-pk').html('#' + product_pk + '--')
    $('#product-ingredinets-choice').html('')
    $('#update-product-btn').show();
    $('#create-product-btn').hide();
    $('#update-product-btn').prop('disabled', false);
    $('#create-product-btn').prop('disabled', true);

    $('#update-product-btn').attr('data-id', product_pk)

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data: {
            'pk': product_pk
        },
        url: GET_PRODUCTS_INGREDIENTS,

        success: function (data) {
            var ingridients = data['ingredients']
            var ingridients_product = data['ingridients_product']
            var categories = data['categories']
            var product_category_pk = data['product_category']
            var product_name = data['name']
            var product_price = data['retail_price']

            $('.product-name2').html(product_name)

            $('#product-name-input').val(product_name);
            $('#product-price').val(product_price);

            var list_keys = []
            for (var i = 0; i < ingridients_product.length; i++) {
                list_keys.push(ingridients_product[i]['pk'])
            }
            for (var i = 0; i < ingridients.length; i++) {
                var temp_ingr = ingridients[i]

                if (list_keys.indexOf(temp_ingr['id']) > -1) {
                    $('#product-ingredinets-choice').append(`
                    <option selected value='`+ temp_ingr['name'] + `' data-id='` + temp_ingr['id'] + `'>` + temp_ingr['name'] + `</option>
                `)
                }
                else {
                    $('#product-ingredinets-choice').append(`
                        <option  value='`+ temp_ingr['name'] + `' data-id='` + temp_ingr['id'] + `'>` + temp_ingr['name'] + `</option>
                    `)
                }
            }
            for (var i = 0; i < categories.length; i++) {

                if (categories[i]['pk'] == product_category_pk) {
                    $('#product-category').append(`
                        <option selected value='`+ categories[i]['name'] + `' data-id='` + categories[i]['pk'] + `'>` + categories[i]['name'] + `</option>
                    `)
                } else {
                    $('#product-category').append(`
                            <option  value='`+ categories[i]['name'] + `' data-id='` + categories[i]['pk'] + `'>` + categories[i]['name'] + `</option>
                    `)
                }
            }

        }
    })

})

$(document).on('click', '#update-product-btn', function () {
    var name = $('#product-name-input').val()
    var ingredients = $('#product-ingredinets-choice').val()
    var category = $('#product-category').val()
    var price = $('#product-price').val()
    var product_pk = $(this).attr('data-id')

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data: {
            'name': name,
            'ingredients[]': ingredients,
            'category': category,
            'price': price,
        },
        url: UPDATE_PRODUCT.replace('0', product_pk),
        success: function (data) {
            $('#' + product_pk).children().eq(0).html(name)
            $('#' + product_pk).children().eq(1).html(category)
            $('#' + product_pk).children().eq(2).html('£' + price)
            $('#product-modal').modal('toggle');
        }
    })


})

$(document).on('click', '#creat-product', function () {

    $('#update-product-btn').hide();
    $('#create-product-btn').show();
    $('#update-product-btn').prop('disabled', true);
    $('#create-product-btn').prop('disabled', false);

    $('#product-name-input').val('')
    $('#product-ingredinets-choice').html('')
    $('#product-category').html('')
    $('#product-price').val('')

    $('.product-pk').html('Create Product')

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        url: GET_PRODUCTS_INGREDIENTS,
        success: function (data) {
            var ingridients = data['ingredients']
            var categories = data['categories']

            for (var i = 0; i < ingridients.length; i++) {
                var temp_ingr = ingridients[i]

                $('#product-ingredinets-choice').append(`
                        <option  value='`+ temp_ingr['name'] + `' data-id='` + temp_ingr['id'] + `'>` + temp_ingr['name'] + `</option>
                    `)

            }
            for (var i = 0; i < categories.length; i++) {

                $('#product-category').append(`
                            <option  value='`+ categories[i]['name'] + `' data-id='` + categories[i]['pk'] + `'>` + categories[i]['name'] + `</option>
                    `)

            }

        }
    })


})

$(document).on('click', '#create-product-btn', function () {

    var name = $('#product-name-input').val()
    var ingredients = $('#product-ingredinets-choice').val()
    var category = $('#product-category').val()
    var price = $('#product-price').val()
    
    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data: {
            'name': name,
            'igredients[]': ingredients,
            'category': category,
            'price': price
        },
        url: CREATE_PRODUCT,
        success: function (data) {


            $('.products-table tbody').append(
                ` 
        <tr id="`+ data['pk'] + `">
            <td scope="row" class="nn-2">`+ name + `</th>
            <td>`+ category + `</td>
            <td>£`+ price + `</td>
            <td>£`+ data['cost'] + `</td>
            <td>
                <button data-id="`+ data['pk'] + `" class="btn btn-info update-product" data-toggle="modal" data-target="#product-modal">Edit</button>
                <button data-id="`+ data['pk'] + `"  class="btn btn-danger btn-delete-product" >Delete</button>
            </td>
        </tr>
        `
            )
            $('#product-modal').modal('toggle');
        }
    })
})

$(document).on('click', '.btn-delete-product', function () {
    var pk = $(this).attr('data-id')
    $(this).parent().parent().remove(); 
    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        url: DELETE_PRODUCT.replace('0', pk),
        success: function (data) {
            
        }
    })
})