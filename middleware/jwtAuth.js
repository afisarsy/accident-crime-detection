const jwt = require('jsonwebtoken');

let Response = require('../models/responseModel');
let User = require('../models/userModel');

module.exports.verifyToken = (req, res, next) => {
    var ip = (req.headers['x-forwarded-for'] || req.connection.remoteAddress || '').split(',')[0].trim();
    var route = req.baseUrl + req.path;

    if (req.headers && req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
        jwt.verify(req.headers.authorization.split(' ')[1], process.env.SECRET, (err, decode) => {
            if (err) {
                req.user = undefined;
            }

            User.findById(decode.id, (err, data) => {
                if (err) {
                    var code = 500;
                    let response = new Response(code, null, null);
                    console.error("%d - %s from %s | %s errors: %s\nRequest data\n%s", code, route, ip, "JWT_AUTH", err, req)
                    res.status(code).send(response);
                } else {
                    console.log(data);
                    req.user = data;
                    next();
                }
            })
        });
    } else {
        req.user = undefined;
        next();
    }
};