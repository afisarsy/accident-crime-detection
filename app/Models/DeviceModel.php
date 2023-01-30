<?php

namespace App\Models;

class DeviceModel extends RESTModel
{

    function __construct() {
        parent::__construct();
    }

    function get_all_devices($headers, $auth)
    {
        //Get all devices (For user with role Admin / Dev only)
        
        $response = $this->http_get('devices/all', $headers, null, null, $auth, null);
        
        return $response;
    }

    function get_devices($headers, $auth)
    {
        //Get user devices from backend
        
        $response = $this->http_get('devices', $headers, null, null, $auth, null);
        
        return $response;
    }

    function get_all_device_data($headers, $auth, $body)
    {
        //Get all device data from backend
        
        $response = $this->http_get('node', $headers, null, null, $auth, $body);
        
        return $response;
    }

    function get_device_data($headers, $pathParams, $auth, $body)
    {
        //Get device data from backend
        
        $response = $this->http_get('node', $headers, $pathParams, null, $auth, $body);
        
        return $response;
    }

    function add_device($headers, $auth, $body)
    {
        //Send new device data to backend
        
        $response = $this->http_post('device/register', $headers, null, null, $auth, $body);
        
        return $response;
    }

    function update_device_property($headers, $pathParams, $auth, $body)
    {
        //Send user device update data to backend
        
        $response = $this->http_put('device', $headers, $pathParams, null, $auth, $body);
        
        return $response;
    }

    function delete_device($headers, $pathParams, $auth, $body)
    {
        //Delete user device data in backend
        
        $response = $this->http_delete('device', $headers, $pathParams, null, $auth, $body);
        
        return $response;
    }
}

?>