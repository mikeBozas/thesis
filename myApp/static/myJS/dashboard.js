$(function() {

    let countDownDate = new Date().getTime() + 1200000;  // + 20min

    $('.renew_button').click(function () {
        $.ajax({url: "/",
                success: function(result){
                    countDownDate = new Date().getTime() + 1200000;
                },
                error: function (xhr, status, error) {
                    countDownDate = new Date().getTime() + 1200000;
                }
        });
    });

    setInterval(function () {
        // Get todays date and time
        let now = new Date().getTime();

        // Find the distance between now an the count down date
        let distance = countDownDate - now;

        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        $('#countdown').html(twoDigits(minutes) + " : " + twoDigits(seconds));

        if(distance < 0){
            $(location).attr('href', '/logout');
        }
    }, 1000);

    function twoDigits(n) {
        return (n < 10 ? '0' : '') + n;
    }

    $('.print_button').click(function () {
      window.print();
    });

    $('.datepicker').datepicker({
      selectMonths: true,
      format: 'mm/yyyy',
      selectYears: false,
      buttonImageOnly: false,
      disable: [true],
      onOpen: function() {
        $(".picker__nav--prev, .picker__nav--next").remove();
      },
      onSet: function( arg ){
        let selectedMonth = parseInt(arg.highlight[1]);
        let selectedYear = arg.highlight[0];
        let selectedDate = arg.highlight[2];
        this.close();
        this.set('select', [selectedYear, selectedMonth, selectedDate,{ format: 'yyyy/mm/dd' }]);
        }
    });

    $('.search_button').click(function () {
        let year_month = $('.ourPicker').val();

        if (year_month === ""){
            $('.ourPicker').val("Please select");
        }
        else {
            $.ajax({
                type: 'GET',
                url: 'year_month_selection',
                data: {
                    'year_month': year_month,
                },
                dataType: 'json',
                success: function (data) {
                       if (data){
                           console.log(data);
                        }
                }
            });
        }
      //  $.ajax({
      //   url: '',
      //   data: {
      //     'username': username
      //   },
      //   dataType: 'json',
      //   success: function (data) {
      //     if (data.is_taken) {
      //       alert("A user with this username already exists.");
      //     }
      //   }
      // });
    });

});
