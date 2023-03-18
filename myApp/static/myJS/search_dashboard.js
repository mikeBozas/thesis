$(function() {

    let temp = $('.total_sales').text().replace(/\,/g,'.');
    $('.total_sales').text(temp);
    $('.success_header').hide();

    $('.collapsible').collapsible({
        accordion: false
    });

    $('#myInput').keyup(function () {
        let filter = $('#myInput').val().toUpperCase();
        let list_items = $('.customer_sale_card');
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

    $('.goal_button').click(function () {
       let total_sales = $('.total_sales').text();
       total_sales = total_sales.toString();
       total_sales = parseFloat(total_sales);

       let goal = (($('.goal_input').val() != "") ? $('.goal_input').val() : 0);

       if (goal){
          // let goal = $('.goal_input').val();
           goal = goal.toString();
           goal = parseFloat(goal);

           let percentage = ((total_sales / goal) * 100).toFixed(2);

           $('.success_percentage').text(percentage);
           $('.success_header').show();
           $('.goal_button').removeClass('red');
       }
       else {
           $('.goal_button').addClass('red');
       }


    });

});