$(function(){
    var tax = TAX;
    tax = tax*100;
    $('.current-tax').append(tax + "%")
    console.log(tax);
})

$(document).on('click', '.change-tax-btn', function(){
    var tax = TAX;
})