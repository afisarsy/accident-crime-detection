<?php

namespace App\Controllers;

use App\Models\DeviceModel;
use Functions\RequestModifier;

class Device extends BaseController
{
    protected $userdata;
    protected $jwtToken;
    protected $device_m;

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

        $this->device_m = new DeviceModel();
    }

    public function get_all()
    {
        $data = [];

        $headers = RequestModifier::get_forward_header($this->request);
        $response = $this->device_m->get_devices($headers, $this->jwtToken);
        if($response->getStatusCode() != 200)
            $data['devices'] = [];
        else
            $data['devices'] = json_decode($response->getBody())->data->devices;

        return $this->response->setJSON($data);
    }

    public function get_all_device_data()
    {
        $data = [];

        $headers = RequestModifier::get_forward_header($this->request);
        parse_str($this->request->getUri()->getQuery(), $queryParams);
        $response = $this->device_m->get_all_device_data($headers, $this->jwtToken, $queryParams);

        if($response->getStatusCode() != 200)
            $data['device_data'] = [];
        else
            $data['device_data'] = json_decode($response->getBody())->data->node_data;

        return $this->response->setJSON($data);
    }

    public function get_device_data($device_id)
    {
        $data = [];

        $headers = RequestModifier::get_forward_header($this->request);
        $pathParams = [$device_id];
        parse_str($this->request->getUri()->getQuery(), $queryParams);
        $response = $this->device_m->get_device_data($headers, $pathParams, $this->jwtToken, $queryParams);

        if($response->getStatusCode() != 200)
            $data['device_data'] = [];
        else
            $data['device_data'] = json_decode($response->getBody())->data->node_data;

        return $this->response->setJSON($data);
    }

    public function add()
    {
        $data = [];

        $headers = RequestModifier::get_forward_header($this->request);
        $requestData = $this->request->getJSON();
        $response = $this->device_m->add_device($headers, $this->jwtToken, $requestData);

        if($response->getStatusCode() != 200)
            $data['msg'] = 'ERROR';
        else
            $data['msg'] = 'OK';

        return $this->response->setStatusCode($response->getStatusCode())->setJSON($data);
    }

    public function update($device_id)
    {
        $headers = RequestModifier::get_forward_header($this->request);
        $pathParams = [$device_id];
        $requestData = $this->request->getJSON();
        $response = $this->device_m->update_device_property($headers, $pathParams, $this->jwtToken, $requestData);

        return $this->response->setStatusCode($response->getStatusCode())->setJSON($response->getBody());
    }

    public function delete($device_id)
    {
        $headers = RequestModifier::get_forward_header($this->request);
        $pathParams = [$device_id];
        $requestData = array('owner_id' => $this->userdata['id']);
        $response = $this->device_m->delete_device($headers, $pathParams, $this->jwtToken, $requestData);

        return $this->response->setStatusCode($response->getStatusCode())->setJSON($response->getBody());
    }
}