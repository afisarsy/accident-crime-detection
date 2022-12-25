var jwt = require("jsonwebtoken");

let DataFunction = require('../functions/dataFunction');
let Response = require('../models/responseModel');
let User = require('../models/userModel');

let debug = require('debug')('app:server:controller:user');

exports.register = (req, res) => {
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
        var response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    let user = new User({
        name: req.body.name,
        username: req.body.username,
        password: DataFunction.hashPassword(req.body.password),
        role: req.body.role || "user"
    });

    User.create(user, (err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 400){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {input: [err.error]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var token = jwt.sign({id: data.id}, process.env.SECRET, {expiresIn: 86400});
            var userData = {
                user: {
                    id: data.id,
                    name: data.name,
                    username: data.username,
                    role: data.role
                }
            };
            var additionalData = {
                accessToken: token
            };

            var code = 200;
            var response = new Response(code, null, userData, additionalData);
            debug("%d - %s from %s | User created: %s", code, route, ip, data);
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
        var response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    User.getAll((err, data) => {
        if (err) {
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: ["No user found"]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            var response = new Response(code, null, {users: data});
            debug("%d - %s from %s | Users: %s", code, route, ip, JSON.stringify(data));
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
        var response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    User.findById(req.user.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`No user with id ${req.user.id} found`]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            var response = new Response(code, null, {user: data});
            debug("%d - %s from %s | User %s Data: %s", code, route, ip, req.user.id, JSON.stringify(data));
            res.status(code).send(response);
        }
    });
}

exports.login = (req, res) => {
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
        var response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors), req);
        res.status(code).send(response);
        return;
    }

    User.findByUsername(req.body.username, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){  //not found in database
                code = 401;             //unauthorized
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", code, route, ip, err.type, err.error, req, err.query);
                message = {input: ["Invalid username"]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
            return;
        }
        else {
            if (DataFunction.checkPassword(req.body.password, data.password)){

                var token = jwt.sign({id: data.id}, process.env.SECRET, {expiresIn: 86400});
                var userData = {
                    user: {
                        id: data.id,
                        name: data.name,
                        username: data.username,
                        role: data.role
                    }
                };
                var additionalData = {
                    accessToken: token
                };

                var code = 200;
                var response = new Response(code, null, userData, additionalData);
                debug("%d - %s from %s | User %s logged in | Data: %s\nAdditional Data:\n%s", code, route, ip, data.username, JSON.stringify(userData), JSON.stringify(additionalData));
                res.status(code).send(response);
            }
            else{
                var code = 401;
                var response = new Response(code, {input: ["Invalid password"]}, null);
                debug("%d - %s from %s | Password %s is wrong | Data: %s", code, route, ip, req.body.password, JSON.stringify(data));
                res.status(code).send(response);
            }
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
        var response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    let input_errors = [];
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
    if (req.body.role){
        update_data.role = req.body.role;
    }
    
    if (Object.keys(update_data).length === 0){
        input_errors.push("No valid data found");
        input_errors.push("Acceptable data: name, username, password, role");
        var code = 400;
        var response = new Response(code, {input: input_errors}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(input_errors));
        res.status(code).send(response);
        return;
    }

    User.updateById(req.user.id, update_data, (err, data) => {
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
                message = {msg: [`No user with id ${req.user.id} found, failed to update user data`]};
            }
            
            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            var response = new Response(code, null, {user: data});
            debug("%d - %s from %s | User %s Updated to: %s", code, route, ip, req.user.id, data);
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
        var response = new Response(code, {auth: auth_error}, null);
        console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s", code, route, ip, response.status, JSON.stringify(auth_error), req);
        res.status(code).send(response);
        return;
    }

    User.removeById(req.user.id, (err, data) => {
        if (err){
            message = null;
            if (err.code == 500){
                console.error("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
            }
            else if (err.code == 404){
                console.warn("%d - %s from %s | %s\nerrors\n%s\nRequest data\n%s\nError Query\n%s", err.code, route, ip, err.type, err.error, req, err.query);
                message = {msg: [`No user with id ${req.user.id} found, failed to delete user`]};
            }

            var response = new Response(err.code, message, null);
            res.status(err.code).send(response);
        } else {
            var code = 200;
            var response = new Response(code, null, null);
            debug("%d - %s from %s | User deleted: %s", code, route, ip, req.user.id);
            res.status(code).send(response);
        }
    });
}