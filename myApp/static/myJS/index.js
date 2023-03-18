$(function(){
    $('input[type=checkbox]').checked = false; // to show password na einai uncheck

    $('.togglePassword').click(function () { // se ka8e click sto show password
        if($('input[type=checkbox]').prop( "checked" )){ // des na einai checked
            $('.password').attr('type', 'text'); // alla3e to type tou input password se text
        }
        else { // an einai uncheck
            $('.password').attr('type', 'password'); // kanei to type tou input password se password
        }
    });

}); // telos JQ