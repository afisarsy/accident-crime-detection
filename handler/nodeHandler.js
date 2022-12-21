let debug = require('debug')('app:mqtt');

let Node = require('../models/nodeModel');

module.exports.store = (topic, deviceId, message) => {
    try{
        let data = JSON.parse(message);
        data.deviceId = deviceId;
        Node.store(data, (err, result) => {
            debug("Device %s data stored at id: %s", deviceId, result.id);
        })
    }
    catch(err) {
        var publish_data = {topic: topic, msg: message};
        console.error("Error from device %s | Store device data failed errors:%s\nPublish data:\n%s\nError Query:\n%s", deviceId, err.error, publish_data, err.query);
        throw err;
    }
}