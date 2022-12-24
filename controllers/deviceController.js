let Response = require('../models/responseModel');
let Device = require('../models/deviceModel');
let debug = require('debug')('app:server:controller:device');

exports.register = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    let input_errors = [];
    if (!req.body.device_id) {
        input_errors.push("missing device_id data");
    }
    if (!req.body.name) {
        input_errors.push("missing name data");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    let device = new Device({
        device_id: req.body.device_id,
        owner_id: req.user.id,
        name: req.body.name,
        description: req.body.description || "",
        last_loc_id: ""
    });

    Device.create(device, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 400){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {input: [err.error]};
            }
            else if (err.code == 404){
                message = {input: [`owner_id = ${req.user.id} not found, failed to create device`]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | Device created: %s", code, route, ip, data);
            res.status(code).send(response);
        }
    })
}

exports.getAll = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
        
        if (["dev", "admin"].indexOf(req.user.role) == -1){
            throw "Unauthorized access";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    Device.getAll((err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["Device not found"]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | Devices: %s", code, route, ip, JSON.stringify(data));
            res.status(code).send(response);
        }
    })
}

exports.getMine = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    Device.findByOwnerId(req.user.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["Device not found"]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | User %s Devices: %s", code, route, ip, req.user.id, JSON.stringify(data));
            res.status(code).send(response);
        }
    });
}

exports.update = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    let input_errors = [];
    if (!req.params.id){
        input_errors.push("missing parameter device_id");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }
    
    var update_data = {};
    if (req.body.device_id){
        update_data.device_id = req.body.device_id;
    }
    if (req.body.name){
        update_data.name = req.body.name;
    }
    if (req.body.description){
        update_data.description = req.body.description;
    }

    if (Object.keys(update_data).length === 0){
        input_errors.push("Valid data not found");
        input_errors.push("Acceptable data: device_id, name, description");
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors));
        res.status(code).send(response);
        return;
    }

    Device.updateById(req.params.id, req.user.id, update_data, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 400){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {input: [err.error]};
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`Device ${req.params.id} for user ${req.user.name} not found, failed to update device`]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | Device %s Updated to: %s", code, route, ip, req.params.id, data);
            res.status(code).send(response);
        }
    });
}

exports.delete = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    try{
        if (!req.user) {
            throw "Invalid JWT token";
        }
    }
    catch(auth_error){
        var code = 403;
        let response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    let input_errors = [];
    if (!req.params.id) {
        input_errors.push("missing parameter id");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    Device.removeById(req.params.id, req.user.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["Device not found, failed to delete device"]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, null);
            debug("%d - %s from %s | Device deleted: %s", code, route, ip, req.params.id);
            res.status(code).send(response);
        }
    });
}