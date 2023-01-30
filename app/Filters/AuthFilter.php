<?php

namespace App\Filters;

use CodeIgniter\Filters\FilterInterface;
use CodeIgniter\HTTP\RequestInterface;
use CodeIgniter\HTTP\ResponseInterface;
use Config\App;
use Functions\Utils;

class AuthFilter implements FilterInterface
{
    /**
    * Declare custom properties to avoid deprecated dynamic
    * properties issue in PHP 8.2 or later which will be
    * removed in 9.0.
    */
    protected $jwtToken;
    protected $user_id, $username, $name, $role;

    function __construct()
    {
        helper(['cookie']);
    }

    public function before(RequestInterface $request, $arguments = null)
    {
        $jwtToken = get_cookie('auth');
        $user_id = get_cookie(('user_id'));
        $username = get_cookie(('username'));
        $name = get_cookie('name');
        $role = get_cookie('role');

        if($jwtToken == ''){
            // Redirect to login page if not logged in
            return redirect()->to(base_url("/auth"));
        }
        else if($user_id == '' || $username == '' || $name == '' || $role == ''){
            //Get User data if not in cookie but has jwt
            return redirect()->to(base_url("/auth/verify"))->withCookies();
        }
    }

    public function after(RequestInterface $request, ResponseInterface $response, $arguments = null)
    {
        // Do something here
    }
}