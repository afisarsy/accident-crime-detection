<?php

namespace App\Models;

use CodeIgniter\Model;
use Functions\StringModifier;

class RESTModel extends Model
{
    protected $client;

    public function __construct()
    {
        parent::__construct();

        $this->client = \Config\Services::curlrequest();
    }

    //====================================================
    //=================REST API functions=================
    //====================================================
    protected function http_request($method, $url, $headers, $pathParams, $queryParams, $auth, $body)
    {
        //Set authorization header if exist
        if (!empty($auth)){
            $headers = array('Authorization' => $auth) + $headers;
        }

        //CURL base config
        $options = [
            'baseURI' => backend_url(),
            'headers' => $headers,
            'http_errors' => false,
            'json' => $body
        ];

        //Modify url with path params and query params
        $url = StringModifier::get_url($url, $pathParams, $queryParams);

        $response = $this->client->request($method, $url, $options);

        return $response;
    }
    
    public function http_get($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('get', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_delete($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('delete', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_head($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('head', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_options($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('options', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_patch($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('patch', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_post($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('post', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
    
    public function http_put($url, $headers, $pathParams = null, $queryParams = null, $auth = null, $body = '')
    {
        return self::http_request('put', $url, $headers, $pathParams, $queryParams, $auth, $body);
    }
}

?>