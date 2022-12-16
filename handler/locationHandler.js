let mqtt = require('../models/mqtt');
let debug = require('debug')('app:mqtt');

let Location = require('../models/locationModel');
let topic = 'amw/location/#';

mqtt.subscribe(topic, (err) => {
    debug('Subscribed to topic : ' + topic);
})

module.exports.store = (id, ownerId, message) => {
    try{
        let data = JSON.parse(message);
        data.deviceId = id;
        data.ownerId = ownerId;
        Location.store(data, (err, result) => {

        })
    }
    catch(err) {
        console.error(err);
        throw err;
    }
}