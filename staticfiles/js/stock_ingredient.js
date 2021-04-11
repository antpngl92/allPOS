$(document).on('click', '.update_ingredients', function(){

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var modal_ingredint_id = '.ingredient_pk'
    var modal_ingredint_name = '.ingredient_name'
    var select_input = '#related-inventory-ingredient-choice'

    cleanField(modal_ingredint_id);
    cleanField(modal_ingredint_name);
    cleanField(select_input);

    var ingredient_id = $(this).data('id');
    var row_data = $('#'+ingredient_id).children()

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

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_INVENTORY_INGREEDIENTS,
        success: function (data) {
           
            data = data['inventory_ingredients']
            for (var i = 0; i < data.length; i++) {

                if (ingredient_related_inventory_ingredient == data[i]['name']){
                    $('#related-inventory-ingredient-choice').append("<option selected value='"+ data[i]['name'] +"' data-id= '" +data[i]['id'] +"'>" +data[i]['name'] + " </option>")
                    continue
                }
                $('#related-inventory-ingredient-choice').append("<option value='" + data[i]['name'] + "' data-id= '" +data[i]['id'] +"'>" +data[i]['name'] + " </option>")
            }
        }
    })
})


function cleanField(field){
    $(field).html(" ")
}