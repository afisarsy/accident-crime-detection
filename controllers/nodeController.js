let Response = require('../models/responseModel');
let Node = require('../models/nodeModel');
let debug = require('debug')('app:server:controller:node');
let {DateTime} = require('luxon');

exports.getAllData = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;
    const timestamp = DateTime.now();

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: [auth_error]}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    let input_errors = [];
    var from = timestamp.toFormat('yyyy-MM-dd 00:00:00');
    var to = timestamp.toFormat('yyyy-MM-dd 23:59:59');
    if (req.body.from){
        if (DateTime.fromFormat(req.body.from, 'yyyy-MM-dd HH:mm:ss').isValid){
            from = req.body.from;
        }
        else{
            input_errors.push("invalid from parameter, datetime with format yyyy-MM-dd HH:mm:ss");
        }
    }
    if (req.body.to){
        if (DateTime.fromFormat(req.body.to, 'yyyy-MM-dd HH:mm:ss').isValid){
            to = req.body.to;
        }
        else{
            input_errors.push("invalid to parameter, datetime with format yyyy-MM-dd HH:mm:ss");
        }
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    Node.findAllDeviceData(req.user.id, from, to, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404 && err.type == 'NODE_DATA_FIND_ALL_0_ROW'){
                debug("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["No Data"]};
            }
            else if (err.code == 404 && err.type == 'USER_HAS_NO_DEVICE_WITH_ID'){
                debug("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [err.error]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, {node_data: data});
            debug("%d - %s from %s | User %s Devices Data from:%s to:%s\n%s", code, route, ip, req.user.id, from, to, JSON.stringify(data));
            res.status(code).send(response);
        }
    })
}

exports.getData = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: [auth_error]}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

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
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    Node.findByDeviceId(req.user.id, req.params.deviceId, limit, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404 && err.type == 'NODE_DATA_FIND_BY_DEVICE_ID_0_ROW'){
                debug("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["No Data"]};
            }
            else if (err.code == 404 && err.type == 'USER_HAS_NO_DEVICE_WITH_ID'){
                debug("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [err.error]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, {node_data: data});
            debug("%d - %s from %s | Device %s Data: %s", code, route, ip, req.params.deviceId, JSON.stringify(data));
            res.status(code).send(response);
        }
    })
}