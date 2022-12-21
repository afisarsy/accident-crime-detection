let debug = require('debug')('app:mqtt:handler:node');
let util = require('util');

let Node = require('../models/nodeModel');

module.exports.store = (topic, deviceId, message) => {
    let data = JSON.parse(message);
    data.device_id = deviceId;
    console.log(`device_id: ${data.device_id}\nmessage received: ${util.inspect(data, {depth: null})}`);
    Node.store(data, (err, res) => {
        if (err){
            var publish_data = {topic: topic, msg: message};
            console.error("Error from device %s | %s errors: %s\nPublish data:\n%s\nError Query:\n%s", deviceId, err.type, err.error, publish_data, err.query);
            return
        }
        debug("Device %s data stored at id: %s", deviceId, res.id);
    });
}