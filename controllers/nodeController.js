let Response = require('../models/responseModel');
let Node = require('../models/nodeModel');
let debug = require('debug')('app:server:controller:node');

exports.findByDeviceId = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    let input_errors = [];
    if (!req.params.deviceId) {
        input_errors.push("missing parameter device id");
    }
    var limit = 7;
    if (req.body.limit){
        try{
            limit = parseInt(req.body.limit);
        }
        catch(err){
            input_errors.push("invalid limit parameter, expecting an int");
        }
    }
    
    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    Node.findByDeviceId(req.params.deviceId, limit, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                debug("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["No Data"]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | Device %s Data: %s", code, route, ip, req.params.deviceId, JSON.stringify(data));
            res.send(response);
        }
    })
}