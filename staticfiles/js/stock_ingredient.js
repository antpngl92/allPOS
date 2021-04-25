$(document).on('click', '.update_ingredients', function () {

    $('#create-ingredient-btn').hide();
    $('#update-ingredient-btn').show();
    $('#create-ingredient-btn').prop('disabled', true);
    $('#update-ingredient-btn').prop('disabled', false);

    var modal_ingredint_id = '.ingredient_pk'
    var modal_ingredint_name = '.ingredient_name'
    var select_input = '#related-inventory-ingredient-choice'

    cleanField(modal_ingredint_id);
    cleanField(modal_ingredint_name);
    cleanField(select_input);

    var ingredient_id = $(this).data('id');
    var row_data = $('#' + ingredient_id).children()

    $('#update-ingredient-btn').attr('data-pk', "")
    $('#update-ingredient-btn').attr('data-pk', ingredient_id)

    var ingredient_name = ($(row_data[0]).text()).replace(/\n|\r/g, "");
    var ingredient_quant = $(row_data[1]).text()
    var ingredient_related_inventory_ingredient = $(row_data[2]).text()

    $(modal_ingredint_id).html('#' + ingredient_id + '--')
    $(modal_ingredint_name).html(ingredient_name)

    $('#ing2-name').val(ingredient_name);
    $('#ing-quant').val(ingredient_quant);

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        url: GET_INVENTORY_INGREEDIENTS,
        success: function (data) {
            data = data['inventory_ingredients']
            for (var i = 0; i < data.length; i++) {

                if (ingredient_related_inventory_ingredient == data[i]['name']) {
                    $('#related-inventory-ingredient-choice').append("<option selected value='"+data[i]['name']+"' data-id= '" + data[i]['id'] + "'>"+data[i]['name']+"</option>")
                    continue
                }
                $("#related-inventory-ingredient-choice").append('<option value="'+data[i]['name']+'" data-id="'+data[i]['id']+'">'+data[i]['name']+'</option>')
            }
        }
    })
})

$(document).on('click', '#update-ingredient-btn', function(){
    var name = $('#ing2-name').val()
    var quantity = $('#ing-quant').val()
    var rii_pk = $('#related-inventory-ingredient-choice option:selected').attr('data-id')
    var ingredient_pk = $(this).attr('data-pk')

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data:{
            'name': name,
            'quantity' : quantity,
            'rii_pk': rii_pk,
        },
        url: UPDATE_INGREDIENT.replace('0', ingredient_pk),
        success: function (data) {
            $($('#'+ ingredient_pk).children().eq(0)).html(name)
            $($('#'+ ingredient_pk).children().eq(1)).html(quantity)
            $($('#'+ ingredient_pk).children().eq(2)).html(data['rii_name'])

            $('#ingredient-modal').modal('toggle');
        }
    })
})

$(document).on('click', '#creat-ingredient', function () {

    $('#related-inventory-ingredient-choice').html('<option value="" disabled selected>Select Related Inventory Ingredient</option>')

    $('#update-ingredient-btn').hide();
    $('#create-ingredient-btn').show();
    $('#create-ingredient-btn').prop('disabled', false);
    $('#update-ingredient-btn').prop('disabled', true);

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var modal_ingredint_id = '.ingredient_pk'
    var modal_ingredint_name = '.ingredient_name'


    cleanField(modal_ingredint_id);
    cleanField(modal_ingredint_name);
    $('#ing2-name').val("")
    $('#ing-quant').val("")

    $(modal_ingredint_name).html("Create new Ingredient")

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_INVENTORY_INGREEDIENTS,
        success: function (data) {

            data = data['inventory_ingredients']
            for (var i = 0; i < data.length; i++) {
                $('#related-inventory-ingredient-choice').append("<option value='" + data[i]['name'] + "' data-id= '" + data[i]['id'] + "'>" + data[i]['name'] + " </option>")
            }
        }
    })

})

$(document).on('click', '#create-ingredient-btn', function(){

    var name = $('#ing2-name').val()
    var quantity = $('#ing-quant').val()
    var rii_pk = $('#related-inventory-ingredient-choice option:selected').attr('data-id')

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        data:{
            'name': name,
            'quantity' : quantity,
            'rii_pk': rii_pk,
        },
        url: CREATE_INGREDIENT,
        success: function (data) {
 
            $('.inventory-table tbody').append(
                ` 
                <tr id="`+data['pk']+`">
                    <td scope="row" class="nn-2">`+name+`</th>
                    <td>`+quantity+`</td>
                    <td>`+data['rii_name']+`</td>
                    <td>
                        <button data-id="`+data['pk']+`" class="btn btn-info update_ingredients" data-toggle="modal" data-target="#ingredient-modal">Edit</button>
                        <button data-id="`+data['pk']+`"  class="btn btn-danger btn-delete-ing" >Delete</button>
                    </td>
                </tr>
                `
            )
            $('#ingredient-modal').modal('toggle');
        }
    })

})

$(document).on('click', '.btn-delete-ing', function(){
    var pk = $(this).attr('data-id')
    $(this).parent().parent().remove(); 
    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        url: DELETE_INGREDIENT.replace('0', pk),
        success: function (data) {
            
        }
    })
})
   
function cleanField(field) {
    $(field).html(" ")
}