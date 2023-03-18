$(function () {

    $('.collapsible').collapsible();

    $('#myInput').keyup(function () {
        let filter = $('#myInput').val().toUpperCase();
        let list_items = $('.insurance_list_item');
        let a;

        for (let i=0; i < list_items.length; i++) {
            a = list_items[i];
            if (a.innerHTML.toUpperCase().indexOf(filter) > -1){
                list_items[i].style.display = "";
            }
            else {
                list_items[i].style.display = "none";
            }
        }
    });

});