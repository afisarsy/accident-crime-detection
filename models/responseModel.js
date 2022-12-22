const HTTP_STATUS = {
    100: "CONTINUE",                                //This interim response indicates that the client should continue the request or ignore the response if the request is already finished.
    101: "SWITCHING_PROTOCOLS",                     //This code is sent in response to an Upgrade request header from the client and indicates the protocol the server is switching to.
    102: "PROCESSING",                              //(WebDAV) This code indicates that the server has received and is processing the request, but no response is available yet.
    103: "EARLY_HINTS",                             //This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response.
    200: "OK",                                      //The request succeeded. The result meaning of "success" depends on the HTTP method: [GET]=The resource has been fetched and transmitted in the message body, [HEAD]=The representation headers are included in the response without any message body, [PUT]or[POST]=The resource describing the result of the action is transmitted in the message body, [TRACE]=The message body contains the request message as received by the server.
    201: "CREATED",                                 //The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
    202: "ACCEPTED",                                //The request has been received but not yet acted upon. It is noncommittal, since there is no way in HTTP to later send an asynchronous response indicating the outcome of the request. It is intended for cases where another process or server handles the request, or for batch processing.
    203: "NON-AUTHORITATIVE_INFORMATION",           //This response code means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy. This is mostly used for mirrors or backups of another resource. Except for that specific case, the 200 OK response is preferred to this status.
    204: "NO_CONTENT",                              //There is no content to send for this request, but the headers may be useful. The user agent may update its cached headers for this resource with the new ones.
    205: "RESET_CONTENT",                           //Tells the user agent to reset the document which sent this request.
    206: "PARTIAL_CONTENT",                         //This response code is used when the Range header is sent from the client to request only part of a resource.
    207: "MULTI-STATUS",                            //(WebDAV) Conveys information about multiple resources, for situations where multiple status codes might be appropriate.
    208: "ALREADY_REPORTED",                        //(WebDAV) Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection.
    226: "IM_USED",                                 //(HTTP Delta encoding) The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.
    300: "MULTIPLE_CHOICES",                        //The request has more than one possible response. The user agent or user should choose one of them. (There is no standardized way of choosing one of the responses, but HTML links to the possibilities are recommended so the user can pick.)
    301: "MOVED_PERMANENTLY",                       //The URL of the requested resource has been changed permanently. The new URL is given in the response.
    302: "FOUND",                                   //This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.
    303: "SEE_OTHER",                               //The server sent this response to direct the client to get the requested resource at another URI with a GET request.
    304: "NOT_MODIFIED",                            //This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.
    //305: "USE_PROXY",                             //Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy.
    //306: "UNUSED",                                //This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification.
    307: "TEMPORARY_REDIRECT",                      //The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request.
    308: "PERMANENT_REDIRECT",                      //This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request.
    400: "BAD_REQUEST",                             //The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).
    401: "UNAUTHORIZED",                            //Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". That is, the client must authenticate itself to get the requested response.
    402: "PAYMENT_REQUIRED",                        //This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists.
    403: "FORBIDDEN",                               //The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401 Unauthorized, the client's identity is known to the server.
    404: "NOT_FOUND",                               //The server cannot find the requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 Forbidden to hide the existence of a resource from an unauthorized client. This response code is probably the most well known due to its frequent occurrence on the web.
    405: "METHOD_NOT_ALLOWED",                      //The request method is known by the server but is not supported by the target resource. For example, an API may not allow calling DELETE to remove a resource.
    406: "NOT_ACCEPTABLE",                          //This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent.
    407: "PROXY_AUTHENTICATION_REQUIRED",           //This is similar to 401 Unauthorized but authentication is needed to be done by a proxy.
    408: "REQUEST_TIMEOUT",                         //This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP pre-connection mechanisms to speed up surfing. Also note that some servers merely shut down the connection without sending this message.
    409: "CONFLICT",                                //This response is sent when a request conflicts with the current state of the server.
    410: "GONE",                                    //This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for "limited-time, promotional services". APIs should not feel compelled to indicate resources that have been deleted with this status code.
    500: "INTERNAL_SERVER_ERROR",                   //The server has encountered a situation it does not know how to handle.
    501: "NOT_IMPLEMENTED",                         //The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD.
    502: "BAD_GATEWAY",                             //This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.
    503: "SERVICE_UNAVAILABLE",                     //The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user-friendly page explaining the problem should be sent. This response should be used for temporary conditions and the Retry-After HTTP header should, if possible, contain the estimated time before the recovery of the service. The webmaster must also take care about the caching-related headers that are sent along with this response, as these temporary condition responses should usually not be cached.
    504: "GATEWAY_TIMEOUT",                         //This error response is given when the server is acting as a gateway and cannot get a response in time.
    505: "HTTP_VERSION_NOT_SUPPORTED",              //The HTTP version used in the request is not supported by the server.
    506: "VARIANT_ALSO_NEGOTIATES",                 //The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process.
    507: "INSUFFICIENT_STORAGE",                    //(WebDAV) The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.
    508: "LOOP_DETECTED",                           //(WebDAV) The server detected an infinite loop while processing the request.
    510: "NOT_EXTENDED",                            //Further extensions to the request are required for the server to fulfill it.
    511: "NETWORK_AUTHENTICATION_REQUIRED",         //Indicates that the client needs to authenticate to gain network access.
}

let Response = function(code, error, data, others=null) {
    this.code = code;
    this.status = HTTP_STATUS[code];
    if (data)
        this.data = data;
    if (error)
        this.error = error;
    for (key in others)
        this[key] = others[key];
}

module.exports = Response;