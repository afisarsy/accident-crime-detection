let Device = require('../models/deviceModel');

exports.create = (req, res) => {
    if (!req.body) {
        res.status(400).send({
            message: "Content can\'t be empty!"
        });
        return;
    }

    let device = new Device({
        device_id: req.body.device_id,
        owner_id: req.body.owner_id,
        name: req.body.name,
        description: req.body.description,
        last_loc_id: ""
    });

    Device.create(device, (err, data) => {
        if (err) {
            res.status(500).send({
                message: err.message || "Error occurred, failed to create device"
            });
        } else {
            res.send(data);
        }
    })
}

exports.findAll = (req, res) => {
    Device.getAll((err, data) => {
        if (err) {
            res.status(500).send({
                message: err.message || "Error occurred, failed to get devices"
            });
        } else {
            res.send(data);
        }
    })
}

exports.findUserDevices = (req, res) => {
    if (!req.params.ownerId) {
        res.status(400).send({
            message: "Owner id can\'t be empty!"
        });
        return;
    }

    Device.findByOwnerId(req.params.ownerId, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "Device with ownerId " + req.params.ownerId + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to get device with ownerId " + req.params.ownerId
                });
            }
        } else {
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

    Device.updateById(req.params.id, req.body, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "Device with id " + req.params.id + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to update device with id " + req.params.id
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
            message: "Device id can\'t be empty!"
        });
        return;
    }

    Device.removeById(req.params.id, (err, data) => {
        if (err){
            if (err.reason === "not_found") {
                res.status(404).send({
                    message: "Device with id " + req.params.id + " not found"
                });
            } else {
                res.status(500).send({
                    message: err.message || "Error occured, failed to delete device with id " + req.params.id
                });
            }
        } else {
            res.send(data);
        }
    });
}