let mqtt = require('../models/mqtt');
let debug = require('debug')('app:mqtt');

let Location = require('../models/locationModel');
let topics = {
    location: process.env.MQTT_BASE_TOPIC + '/location/#'
};

mqtt.subscribe(topics['location'], (err) => {
    debug('Subscribed to topic : ' + topics['location']);
})

module.exports.topics = topics

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