$(document).ready(function(){

    $('#id_old_password').parent().insertAfter($('#id_email').parent())
    $('#id_new_password1').parent().insertAfter($('#id_change_password').parent())
    $('#id_new_password2').parent().insertAfter($('#id_new_password1').parent())
    $('#id_old_password').prev().text('Password');

    $('#id_new_password1').parent().hide();
    $('#id_new_password2').parent().hide();

    $('#id_change_password').change(function() {

        if (this.checked) {
            $('#id_new_password1').parent().show();
            $('#id_new_password2').parent().show();
            $('#id_old_password').prev().text('Old Password');
            $('#id_new_password1').val('');
            $('#id_new_password2').val('');
        }
        else {
            $('#id_new_password1').parent().hide();
            $('#id_new_password2').parent().hide();
            $('#id_old_password').prev().text('Password');
            $('#id_new_password1').val('dummyPass3');
            $('#id_new_password2').val('dummyPass3');
        }
    });

});