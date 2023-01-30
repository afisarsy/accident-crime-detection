<?php

namespace App\Controllers;

use App\Models\UserModel;
use Functions\ArrayModifier;
use Functions\RequestModifier;

class Auth extends BaseController
{
    protected $user_m;

    public function __construct()
    {
        helper(['cookie']);
        
        $this->user_m = new UserModel();
    }

    public function index()
    {
        $data = [];

        if(!empty($this->session->get('register'))){
            $data['register'] = $this->session->get('register');
        }
        
        if(!empty($this->session->get('duplicateUsername'))){
            $data['duplicateUsername'] = $this->session->get('duplicateUsername');
        }
        
        if(!empty($this->session->get('authentication'))){
            $data['authentication'] = $this->session->get('authentication');
        }

        return view('pages/auth', $data);
    }

    public function register()
    {
        //Register to backend
        $headers = RequestModifier::get_forward_header($this->request);
        $response = $this->user_m->register($headers, $this->request->getPost());

        if($response->getStatusCode() == 400 && ArrayModifier::array_contains_substrings(json_decode($response->getBody())->error->input, ['Username isn\'t available']))
            return redirect()->to(base_url('/auth'))->with('duplicateUsername',  'Username isn\'t available')->with('register', true)->withInput();

        $jwtToken = 'Bearer ' . json_decode($response->getBody())->accessToken;
        $user_m_id = json_decode($response->getBody())->data->user->id;
        $username = json_decode($response->getBody())->data->user->username;
        $name = json_decode($response->getBody())->data->user->name;
        $role = json_decode($response->getBody())->data->user->role;

        //Set Cookies if Valid
        set_cookie('auth', $jwtToken);
        set_cookie('user_id', $user_m_id);
        set_cookie('username', $username);
        set_cookie('name', $name);
        set_cookie('role', $role);

        return redirect()->to(base_url())->withCookies();
    }

    public function login()
    {
        //Login to backend
        $headers = RequestModifier::get_forward_header($this->request);
        $response = $this->user_m->login($headers, $this->request->getPost());
        if($response->getStatusCode() != 200)
            return redirect()->to(base_url('/auth'))->with('authentication',  'Invalid Username or Password')->withInput();

        $jwtToken = 'Bearer ' . json_decode($response->getBody())->accessToken;
        $user_id = json_decode($response->getBody())->data->user->id;
        $username = json_decode($response->getBody())->data->user->username;
        $name = json_decode($response->getBody())->data->user->name;
        $role = json_decode($response->getBody())->data->user->role;

        //Set Cookies if Valid
        set_cookie('auth', $jwtToken);
        set_cookie('user_id', $user_id);
        set_cookie('username', $username);
        set_cookie('name', $name);
        set_cookie('role', $role);

        return redirect()->to(base_url())->withCookies();
    }

    public function logout()
    {
        //Delete Login Cookies
        delete_cookie('auth');
        delete_cookie('user_id');
        delete_cookie('username');
        delete_cookie('name');
        delete_cookie('role');
        
        return redirect()->to(base_url())->withCookies();
    }

    public function verify()
    {
        //Verify saved JWT to backend
        $headers = RequestModifier::get_forward_header($this->request);
        $jwtToken = get_cookie('auth');
        $response = $this->user_m->get_data($headers, $jwtToken);

        if($response->getStatusCode() == 401){
            return redirect()->to(base_url('/auth'))->with('authentication',  'Incorrect username or password')->withInput();
        }
        
        $user_id = json_decode($response->getBody())->data->user->id;
        $name = json_decode($response->getBody())->data->user->name;
        $role = json_decode($response->getBody())->data->user->role;

        //Set Cookies if Valid
        set_cookie('user_id', $user_id);
        set_cookie('name', $name);
        set_cookie('role', $role);

        return redirect()->to(base_url())->withCookies();
    }
}