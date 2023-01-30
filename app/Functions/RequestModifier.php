<?php

namespace Functions;

use CodeIgniter\HTTP\Header;
use CodeIgniter\HTTP\RequestInterface;

class RequestModifier
{
    public static function get_forward_header(RequestInterface $request): array
    {
        //Scrap http header from user request

        $headers = array();
        $headers['Content-Type'] = 'application/json';
        $headers['Host'] = $request->getUri()->getHost();
        $headers['User-Agent'] = $request->getUserAgent()->getAgentString();
        $headers['Accept-Encoding'] = $request->getHeaderLine('accept-encoding');
        $headers['X-Forwarded-For'] = $request->getIPAddress();
        $headers['X-Forwarded-Host'] = $request->getServer('HTTP_HOST');
        $headers['X-Forwarded-Proto'] = strtolower(explode('/', $request->getServer('SERVER_PROTOCOL'))[0]);

        return $headers;
    }
}

?>