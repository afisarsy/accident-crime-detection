$(document).ready(() => {
    //Toggle login/register form
    $('.login-form-toggle').click((e) => {
        e.preventDefault();
        $('#container-login').toggleClass('hidden');
        $('#container-register').toggleClass('hidden');
    })
    
    //Input filtering
    $('#loginUsername,#registerUsername').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_]+$");
    })
    $('#registerName').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_ @#().,]+$");
    })

    //Login
    $('#btnLogin').click(function(e) {
        e.preventDefault();
        var error = 0;

        var username = $('#loginUsername').val();
        var password = $('#loginPassword').val();

        if(username == ''){
            $('#loginUsername').addClass('is-invalid');
            $('#loginUsernameError').html('Username can\'t be empty');
            error += 1;
        }
        else{
            $('#loginUsername').removeClass('is-invalid');
            $('#loginUsernameError').html(' ');
        }

        if(password == ''){
            $('#loginPassword').addClass('is-invalid');
            $('#loginPasswordError').html('Password can\'t be empty');
            error += 1;
        }
        else{
            $('#loginPassword').removeClass('is-invalid');
            $('#loginPasswordError').html(' ');
        }

        if(error == 0){
            $('#loginForm').submit();
        }
    })

    //Register
    $('#btnRegister').click(function(e) {
        e.preventDefault();
        var error = 0;

        var name = $('#registerName').val();
        var username = $('#registerUsername').val();
        var password = $('#registerPassword').val();
        var cpassword = $('#registerCPassword').val();

        if(name == ''){
            $('#registerName').addClass('is-invalid');
            $('#registerNameError').html('Name can\'t be empty');
            error += 1;
        }
        else{
            $('#registerName').removeClass('is-invalid');
            $('#registerNameError').html(' ');
        }

        if(username == ''){
            $('#registerUsername').addClass('is-invalid');
            $('#registerUsernameError').html('Username can\'t be empty');
            error += 1;
        }
        else{
            $('#registerUsername').removeClass('is-invalid');
            $('#registerUsernameError').html(' ');
        }

        if(password == ''){
            $('#registerPassword').addClass('is-invalid');
            $('#registerPasswordError').html('Password can\'t be empty');
            error += 1;
        }
        else{
            $('#registerPassword').removeClass('is-invalid');
            $('#registerPasswordError').html(' ');
        }

        if(cpassword == ''){
            $('#registerCPassword').addClass('is-invalid');
            $('#registerCPasswordError').html('Password can\'t be empty');
            error += 1;
        }
        else if(cpassword != password){
            $('#registerCPassword').addClass('is-invalid');
            $('#registerCPasswordError').html('Password didn\'t match');
            error += 1;
        }
        else{
            $('#registerCPassword').removeClass('is-invalid');
            $('#registerCPasswordError').html(' ');
        }

        if(error == 0){
            $('#registerForm').submit();
        }
    })
});