$(function() {

    $('.datepicker').datepicker({
        autoClose: true,
        format: 'yyyy-mm-dd',
        yearRange: 150,
    });

    $('#ageInput').focus(function () {
        let dateBirth = $('#dateOfBirthInput').val();

        let yearOfDateOfBirthInput = 0;

        if (dateBirth.length){
            yearOfDateOfBirthInput = dateBirth.substr(0,4);
            yearOfDateOfBirthInput = parseInt(yearOfDateOfBirthInput);
        }

        yearOfDateOfBirthInput = (new Date).getFullYear() - yearOfDateOfBirthInput;

        $('#ageInput').val(yearOfDateOfBirthInput);
    });

});