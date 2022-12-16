let Location = require('../models/locationModel');

exports.findByDeviceId = (req, res) => {
    if (!req.params.deviceId) {
        res.status(400).send({
            message: "Device id can\'t be empty!"
        });
        return;
    }

    Location.findByDeviceId(req.params.deviceId, (err, data) => {
        if (err) {
            res.status(500).send({
                message: err.message || "Error occured, failed to get location from device " + req.params.deviceId
            });
        } else {
            res.send(data);
        }
    })
}