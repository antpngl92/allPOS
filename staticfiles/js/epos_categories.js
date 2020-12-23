$(document).on('click','.cat-butt', function(){
    category_pk = $(this).attr('data-id')
    $.ajax({
        method  : "GET",
        url     : GET_CATEGORY.replace("0", category_pk),
        success : function(data){
            var products_buttons = ""
            // console.log(data[0]['id'])
            for(var i = 0; i < data.length; i++){
                products_buttons += '\n<button type="button" data-id="'+data[i]['id']+'" class="product-butt">'+data[i]['product_name']+' <span>£'+data[i]['retail_price']+'</span> </button>'
            }
            $('.products-buttons-row').html(products_buttons)

        } 
    })
})    