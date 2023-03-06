let debug = require('debug')('ACD:mqtt');
debug.log = console.log.bind(console)

let mqtt = require('../models/mqtt');
let Node = require('./nodeHandler')

let topics = {
    node: process.env.MQTT_BASE_TOPIC + '/node'
};

mqtt.subscribe(`${topics['node']}/#`, (err) => {
    debug(`Subscribed to topic : ${topics['node']}/#`);
})

mqtt.on('message', (topic, message) => {
    message = message.toString('utf-8');

    if(topic.indexOf(topics['node']) != -1){
        let node_topic = topic.split(`${topics['node']}/`)[1];
        let topic_params = node_topic.split('/');
        let deviceId = topic_params[0];
        debug("topic: %s | deviceId:%s | message: %s", topic, deviceId, message);
        Node.store(topic, deviceId, message);
    }
})