<?php

namespace App\Controllers;

class Dashboard extends BaseController
{
    protected $userdata;

    public function __construct()
    {
        helper(['cookie']);
        
        $this->userdata = array(
            'id' => get_cookie('user_id'),
            'username' => get_cookie('username'),
            'name' => get_cookie('name'),
            'role' => get_cookie('role')
        );
    }

    public function index()
    {
        $data = [];

        parse_str($this->request->getUri()->getQuery(), $queryParams);
        if (count($queryParams) > 0){
            $mapcenter = [$queryParams['lat'], $queryParams['lng']];
            $zoom = 17;
        }

        $data['nav_title'] = 'Dashboard';
        $data['user'] = $this->userdata;
        $data['map_center'] = isset($mapcenter) ? $mapcenter : [-2, 117.5];
        $data['zoom'] = isset($zoom) ? $zoom : 5;

        return view('pages/map', $data);
    }
    
    public function devices()
    {
        $data = [];
        $data['nav_title'] = 'Devices';
        $data['user'] = $this->userdata;

        return view('pages/devices', $data);
    }
}
