<?php

namespace App\Models;

class UserModel extends RESTModel
{

    function __construct() {
        parent::__construct();
    }

    function get_all_users($headers, $auth)
    {
        //Get all users (For user with role Admin / Dev only)

        $response = $this->http_get('users', $headers, null, null, $auth, null);

        return $response;
    }

    function register($headers, $body)
    {
        //Send register data to backend
        
        $response = $this->http_post('register', $headers, null, null, null, $body);
        
        return $response;
    }

    function login($headers, $body)
    {
        //Send login data to backend
        
        $response = $this->http_post('login', $headers, null, null, null, $body);
        
        return $response;
    }

    function get_data($headers, $auth)
    {
        //Get logged in user data

        $response = $this->http_get('user', $headers, null, null, $auth, null);

        return $response;
    }

    function update_user($headers, $auth, $body)
    {
        //Send user device update data to backend
        
        $response = $this->http_put('user', $headers, null, null, $auth, $body);
        
        return $response;
    }

    function delete_user($headers, $auth, $body)
    {
        //Delete user device data in backend
        
        $response = $this->http_delete('user', $headers, null, null, $auth, $body);
        
        return $response;
    }
}

?>