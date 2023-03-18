$(function() {

    let year = new Date().getFullYear();
    let month = new Date().getMonth() + 1;
    let day = new Date().getDate();

    $('.datepicker').val(year + "-" + month + "-" + day);

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        yearRange: 150,
    });

    $('select').formSelect();
    $('.modal').modal();

    $('#myInput').keyup(function () {
        let filter = $('#myInput').val().toUpperCase();
        let list_items = $('.customer_list_item');
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

    $('.customer_list_item').click(function () {
        let text = "";
        let i = 0;
        $(this).children().each(function () {
            if(i === 1){
                text = text + ", ";
            }
                text = text + $(this).text();
            i++;
        });
        $('#customerInput').val(text);
    });

    $('.new_customer_button').click(function () {
        window.location.href = "new_customer";
    });

});