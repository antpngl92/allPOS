$(document).on('click','.update_ingredient', function(){

    var modal_ingredint_id = '.inventory_ingredient_pk'
    var modal_ingredint_name = '.inventory_ingredient_name'
    var select_input = '#suplier_choice'
    var select_input_parent = '.select-supplier'
    var checkbox_auto = '.checkbox-auto'

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    cleanField(modal_ingredint_id);
    cleanField(modal_ingredint_name);
    cleanField(select_input);
    cleanField(select_input_parent);
    cleanField(checkbox_auto);

    var ingredient_id = $(this).data('id');
    var row_data = $('#'+ingredient_id).children()

    $('#update-inventory-ingredient-btn').attr('data-pk', "")
    $('#update-inventory-ingredient-btn').attr('data-pk', ingredient_id)

    var ingredient_name = ($(row_data[0]).text()).replace(/\n|\r/g, "");
    var ingredient_supp = $(row_data[1]).text()
    var ingredient_cost = $(row_data[2]).text()
    var ingredient_weight = $(row_data[3]).text()
    var ingredient_stock = $(row_data[4]).text()
    var ingredient_stock_needed = $(row_data[5]).text()
    var ingredient_auto = $(row_data[6]).text()

    $(modal_ingredint_id).html('#' + ingredient_id + '--')
    $(modal_ingredint_name).html(ingredient_name)

    $('#ing-name').val(ingredient_name);
    $('#ing-cost').val(ingredient_cost);
    $('#ing-weight').val(ingredient_weight);
    $('#ing-stock').val(ingredient_stock);
    $('#ing-stock-needed').val(ingredient_stock_needed);

    if(ingredient_auto == "True"){
        $('.checkbox-auto').append('<input class="auto_check" type="checkbox" checked><span></span>')
    }else{
        $('.checkbox-auto').append('<input class="auto_check" type="checkbox" ><span></span>')
    }

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_SUPPLIERS,
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                if (ingredient_supp == data[i]['name']){
                    $('#suplier_choice').append("<option selected value='"+ data[i]['name'] +"' data-id= '" +data[i]['id'] +"'>" +data[i]['name'] + " </option>")
                    continue
                }
                $('#suplier_choice').append("<option value='" + data[i]['name'] + "' data-id= '" +data[i]['id'] +"'>" +data[i]['name'] + " </option>")
            }
        }
    })
})



$(document).on('click','#update-inventory-ingredient-btn', function(){
    
    var pk = $(this).attr('data-pk')
    var row_data = $('#'+pk).children() 
    var ingredient_name = $('#ing-name').val()
    var ingredient_supp = $('.select-supplier option:selected').data('id')
    var ingredient_cost =  $('#ing-cost').val();
    var ingredient_weight =  $('#ing-weight').val();
    var ingredient_stock = $('#ing-stock').val();
    var ingredient_stock_needed = $('#ing-stock-needed').val();
    var ingredient_auto = $('.auto_check').is(':checked')
    var ingredient_supp_name = $('.select-supplier option:selected').html()

    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        content_type:'application/json',
        data :{
            'name':ingredient_name,
            'supplier':ingredient_supp,
            'cost' : ingredient_cost,
            'weight' : ingredient_weight,
            'stock' : ingredient_stock, 
            'min_stock': ingredient_stock_needed,
            'automated' : ingredient_auto
        },
        url: UPDATE_INGREDIENT.replace("0",pk),
        success: function (data) {

            ingredient_auto = ingredient_auto.toString()
            ingredient_auto = ingredient_auto.substr(0,1).toUpperCase() + ingredient_auto.substr(1);
        
            $(row_data[0]).html(ingredient_name)

            $(row_data[1]).html(ingredient_supp_name)
            $(row_data[2]).html(ingredient_cost)
            $(row_data[3]).html(ingredient_weight)
            $(row_data[4]).html(ingredient_stock)
            $(row_data[5]).html(ingredient_stock_needed)
            $(row_data[6]).html(ingredient_auto)

            $('#inventory-ingredient-modal').modal('toggle');
        }
    })
})


$(document).on('click', '#creat-inventory-ingredient',function(){

    $('#ing-name-crt').val('');
    $('#ing-cost-crt').val('');
    $('#ing-weight-crt').val('');
    $('#ing-stock-crt').val('');
    $('#ing-stock-needed-crt').val('');
    $('#suplier_choice_crt').html('<option value="" disabled selected>Select suplier</option>')

    var check_box_auto = ".checkbox-auto-crt"
    cleanField(check_box_auto)
    $(check_box_auto).append('<input class="auto_check_crt" type="checkbox" ><span></span>')

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $('#create-inventory-ingridient-modal-header').html("Create Inventory Ingredient")
    $('.inventory_ingredient_name').html("")

    $.ajax({
        method: "GET",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: GET_SUPPLIERS,
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                $('#suplier_choice_crt').append("<option value='" + data[i]['name'] + "' data-id= '" +data[i]['id'] +"'>" +data[i]['name'] + " </option>")
            }
            
        }
    })
})

$(document).on('click', '#create-inventory-ingredient-btn', function(e){
    
    var ingredient_name = $('#ing-name-crt').val()
    var ingredient_supp = $('.select-supplier_crt option:selected').data('id')
    var ingredient_cost =  $('#ing-cost-crt').val();
    var ingredient_weight =  $('#ing-weight-crt').val();
    var ingredient_stock = $('#ing-stock-crt').val();
    var ingredient_stock_needed = $('#ing-stock-needed-crt').val();
    var ingredient_auto = $('.auto_check_crt').is(':checked')


    $.ajax({
        method: "POST",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        content_type:'application/json',
        data :{
            'name':ingredient_name,
            'supplier':ingredient_supp,
            'cost' : ingredient_cost,
            'weight' : ingredient_weight,
            'stock' : ingredient_stock, 
            'min_stock': ingredient_stock_needed,
            'automated' : ingredient_auto
        },
        url: CREATE_INGREDIENT,
        success: function (data) {
            ingredient_auto = ingredient_auto.toString()
            ingredient_auto = ingredient_auto.substr(0,1).toUpperCase() + ingredient_auto.substr(1);
            $('.stock-table tbody').append(`
            <tr id="`+data['pk']+`">
                <td scope="row" class="nn-2">`+ ingredient_name+`</th>
                <td>`+data['sup']+`</td>
                <td>`+ingredient_cost+`</td>
                <td>`+ingredient_weight+`</td>
                <td>`+ingredient_stock+`</td>
                <td>`+ingredient_stock_needed+`</td>
                <td>`+ingredient_auto+`</td>
                <td><button data-id="`+data['pk']+`" class="btn btn-info update_ingredient" data-toggle="modal" data-target="#inventory-ingredient-modal">Edit</button>
                    <button data-id="`+data['pk']+`"  class="btn btn-danger btn-delete" >Delete</button></td>
                </td>
            </tr>`)

            $('#inventory-ingredient-modal-create').modal('toggle');
        }
    })
})

$(document).on('click', '.btn-delete', function(){
    var pk = $(this).attr('data-id')
    $(this).parent().parent().remove();    
    $.ajax({
        method: "DELETE",
        beforeSend: function (xhr) {

            xhr.setRequestHeader('X-CSRFToken', jQuery("[name=csrfmiddlewaretoken]").val());
        },
        content_type:'application/json',
        url: DELETE_INGREDIENT.replace("0", pk),
        success: function (data) {
            
        }
    })
})

function cleanField(field){
    $(field).html(" ")
}