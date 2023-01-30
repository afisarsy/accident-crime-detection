<?php

namespace Functions;

use Functions\ArrayModifier;

class StringModifier
{
    public static function get_url(string $url, array $pathParams = null, array $queryParams = null): string
    {
        //Return url based on path parameters and query parameters
        
        //Add trailing slash if not exist
        if($url[-1] != '/')
            $url .= '/';
        
        //Add path params if exist
        if(!empty($pathParams))
            $url .= join('/', $pathParams);
        
        //Add query params if exist
        if(!empty($queryParams)){
            $url .= '?';
            $url .= join('&', ArrayModifier::associative_2_indexed_array($queryParams));
        }
        
        return $url;
    }
}

?>