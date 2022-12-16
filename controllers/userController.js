let User = require('../models/userModel');

exports.create = (req, res) => {
    if (!req.body) {
        res.status(400).send({
            message: "Content can\'t be empty!"
        });
        return;
    }

    let user = new User({
        name: req.body.name,
        username: req.body.username,
        password: req.body.password
    });

    User.create(user, (err, data) => {
        if (err) {
            res.status(500).send({
                message: err.message || "Error occurred, failed to create user"
            });
        } else {
            res.send(data);
        }
    })
}

exports.findAll = (req, res) => {
    User.getAll((err, data) => {
        if (err) {
            res.status(500).send({
                message: err.message || "Error occurred, failed to get users"
            });
        } else {
            res.send(data);
        }
    })
}

exports.findOne = (req, res) => {
    if (!req.params.id) {
        res.status(400).send({
            message: "User id can\'t be empty!"
        });
        return;
    }

    User.findById(req.params.id, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "User with id " + req.params.id + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to get user with id " + req.params.id
                });
            }
        } else {
            res.send(data);
        }
    });
}

exports.findByAuth = (req, res) => {
    if (!req.body.username || !req.body.password) {
        res.status(400).send({
            message: "Username/Password can\'t be empty!"
        });
        return;
    }

    User.findByUserPass(req.body.username, req.body.password, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "User not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to get user with username " + req.body.username + " and password " + req.body.password
                });
            }
        }
        else {
            res.send(data);
        }
    });
}

exports.update = (req, res) => {
    if (!req.body || !req.params.id) {
        res.status(400).send({
            message: "Content can\'t be empty!"
        });
        return;
    }

    User.updateById(req.params.id, req.body, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "User with id " + req.params.id + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to update user with id " + req.params.id
                });
            }
        } else {
            res.send(data);
        }
    });
}

exports.delete = (req, res) => {    
    if (!req.params.id) {
        res.status(400).send({
            message: "User id can\'t be empty!"
        });
        return;
    }

    User.removeById(req.params.id, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "User with id " + req.params.id + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to delete user with id " + req.params.id
                });
            }
        } else {
            res.send(data);
        }
    });
}