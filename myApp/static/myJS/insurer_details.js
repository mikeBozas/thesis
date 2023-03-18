$(function () {
    $('.collapsible').collapsible({
        accordion: false
    });

    $('#myInput').keyup(function () {
        let filter = $('#myInput').val().toUpperCase();
        let list_items = $('.insurance_sale_card');
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

    $('.datepicker').datepicker({
      format: 'mm/yyyy'
    });

    $('.search_by_date_button').click(function () {
       let date = ($('#myInputMonth').val() != "" ? $('#myInputMonth').val() : 0);

       if (date){
           $('.search_by_date_button').removeClass("red");
       }
       else {
           $('.search_by_date_button').addClass("red");
       }

    });


});