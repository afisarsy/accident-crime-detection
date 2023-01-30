$(document).ready(() => {
    //Input filtering
    $('#username').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_]+$");
    })
    $('#name').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_ @#().,]+$");
    })

    //Enable update button if form data changed
    $('#accountDetailForm input').one('change', function(e) {
        $('#btnUserUpdate').removeClass('disabled');
    })

    //Update account
    $('#btnUserUpdate').click((e) => {
        e.preventDefault();
        var error = 0;

        var username = $('#username').val();
        var name = $('#name').val();
        var role = $('#role').val();
        var password = $('#password').val();
        var cpassword = $('#cpassword').val();

        if(username == ''){
            $('#username').addClass('is-invalid');
            $('#usernameError').html('Username can\'t be empty');
            error += 1;
        }
        else{
            $('#username').removeClass('is-invalid');
            $('#usernameError').html(' ');
        }

        if(name == ''){
            $('#name').addClass('is-invalid');
            $('#nameError').html('Name can\'t be empty');
            error += 1;
        }
        else{
            $('#name').removeClass('is-invalid');
            $('#nameError').html(' ');
        }

        if(role == ''){
            $('#role').addClass('is-invalid');
            $('#roleError').html('Role can\'t be empty');
            error += 1;
        }
        else{
            $('#role').removeClass('is-invalid');
            $('#roleError').html(' ');
        }

        if(cpassword == ''){
            $('#cpassword').addClass('is-invalid');
            $('#cpasswordError').html('Password is required');
            error += 1;
        }
        else{
            $('#cpassword').removeClass('is-invalid');
            $('#cpasswordError').html(' ');
        }

        if(error == 0){
            newData = {
                cpassword: cpassword
            };

            //Ignore if not changed
            if (username != window.decodeURIComponent($.cookie('username'))){
                newData.username = username;
            }
            if (name != window.decodeURIComponent($.cookie('name'))){
                newData.name = name;
            }
            if (role != window.decodeURIComponent($.cookie('role'))){
                newData.role = role;
            }
            if (password != ''){
                newData.password = password;
            }

            //If the user changed some data
            if (Object.keys(newData).length > 1){
                $('#UpdateError').addClass('hidden');

                $('#accountDetailForm').attr('action', '/user/update').submit();
            }
            else{
                $('#UpdateError').removeClass('hidden');
            }
        }
    });

    //Delete Account
    $('#btnUserDelete').click(function(e) {
        e.preventDefault();
        
        $('#accountDetailForm').attr('action', '/user/delete').submit();
    })
});