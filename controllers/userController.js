let Response = require('../models/responseModel');
let User = require('../models/userModel');
let debug = require('debug')('app:server:controller:user');

exports.create = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;
    
    let input_errors = [];
    if (!req.body.name) {
        input_errors.push("missing name data");
    }
    if (!req.body.username) {
        input_errors.push("missing username data");
    }
    if (!req.body.password) {
        input_errors.push("missing password data");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    let user = new User({
        name: req.body.name,
        username: req.body.username,
        password: req.body.password
    });

    User.create(user, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 400){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {input: [err.error]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | User created: %s", code, route, ip, data);
            res.send(response);
        }
    })
}

exports.findAll = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    User.getAll((err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["No user found"]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | Users: %s", code, route, ip, JSON.stringify(data));
            res.send(response);
        }
    })
}

exports.findOne = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    let input_errors = [];
    if (!req.params.id) {
        input_errors.push("missing parameter id");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    User.findById(req.params.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`No user with id ${req.params.id} found`]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | User %s Data: %s", code, route, ip, req.params.id, JSON.stringify(data));
            res.send(response);
        }
    });
}

exports.findByAuth = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    let input_errors = [];
    if (!req.body.username) {
        input_errors.push("missing username data");
    }
    if (!req.body.password) {
        input_errors.push("missing password data");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    User.findByUserPass(req.body.username, req.body.password, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["Incorrect username or password"]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        }
        else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | User %s logged in | Data: %s", code, route, ip, req.params.id, JSON.stringify(data));
            res.send(response);
        }
    });
}

exports.update = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    let input_errors = [];
    if (!req.params.id){
        input_errors.push("missing parameter id");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    var update_data = {};
    if (req.body.name){
        update_data.name = req.body.name;
    }
    if (req.body.username){
        update_data.username = req.body.username;
    }
    if (req.body.password){
        update_data.password = req.body.password;
    }
    
    if (Object.keys(update_data).length === 0){
        input_errors.push("No valid data found");
        input_errors.push("Acceptable data: name, username, password");
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors));
        res.status(code).send(response);
        return;
    }

    User.updateById(req.params.id, update_data, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 400){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {input: [err.error]};
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`No user with id ${req.params.id} found, failed to update user data`]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, data);
            debug("%d - %s from %s | User %s Updated to: %s", code, route, ip, req.params.id, data);
            res.send(response);
        }
    });
}

exports.delete = (req, res) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    let input_errors = [];
    if (!req.params.id) {
        input_errors.push("missing parameter id");
    }

    if (input_errors.length > 0){
        var code = 400;
        let response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    User.removeById(req.params.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s errors: %s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`No user with id ${req.params.id} found, failed to delete user`]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            let response = new Response(code, null, null);
            debug("%d - %s from %s | User deleted: %s", code, route, ip, req.params.id);
            res.send(response);
        }
    });
}