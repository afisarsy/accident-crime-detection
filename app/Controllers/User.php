<?php

namespace App\Controllers;

use App\Models\UserModel;
use Functions\RequestModifier;
use stdClass;

class User extends BaseController
{
    protected $userdata;
    protected $jwtToken;
    protected $user_m;

    public function __construct()
    {
        helper(['cookie']);
        
        $this->userdata = array(
            'id' => get_cookie('user_id'),
            'username' => get_cookie('username'),
            'name' => get_cookie('name'),
            'role' => get_cookie('role')
        );

        $this->jwtToken = get_cookie('auth');

        $this->user_m = new UserModel();
    }
    
    public function index()
    {
        $data = [];
        
        $data['user'] = $this->userdata;

        if(!empty($this->session->get('wrongPassword'))){
            $data['wrongPassword'] = $this->session->get('wrongPassword');
        }

        return view('pages/user', $data);
    }

    public function update()
    {
        //Update
        $headers = RequestModifier::get_forward_header($this->request);
        $loginData = array(
            'username' => $this->userdata['username'],
            'password' => $this->request->getPost()['cpassword']
        );
        $loginResponse = $this->user_m->login($headers, $loginData);
        if($loginResponse->getStatusCode() != 200)
            return redirect()->to(base_url('/user'))->with('wrongPassword',  true)->withCookies()->withInput();

        $requestData = $this->request->getPost();
        $response = $this->user_m->update_user($headers, $this->jwtToken, $requestData);
        if ($response->getStatusCode() == 200){
            if (isset($requestData['username'])){
                set_cookie('username', $requestData['username']);
            }
            if (isset($requestData['name'])){
                set_cookie('name', $requestData['name']);
            }
            if (isset($requestData['role'])){
                set_cookie('role', $requestData['role']);
            }
        }

        return redirect()->to(base_url('/user'))->withCookies();
    }

    public function delete()
    {
        $headers = RequestModifier::get_forward_header($this->request);
        $requestData = $this->request->getJSON();
        $response = $this->user_m->delete_user($headers, $this->jwtToken, $requestData);

        return redirect()->to(base_url('/auth/logout'))->withCookies();
    }
}