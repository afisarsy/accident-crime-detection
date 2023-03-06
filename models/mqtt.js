let mqtt = require('mqtt');
let debug = require('debug')('ACD:mqtt');
debug.log = console.log.bind(console)

let config = {
    host: process.env.MQTT_HOST || 'localhost',
    port: process.env.MQTT_PORT || 3306,
    username: process.env.MQTT_USER,
    password: process.env.MQTT_PASS,
    reconnectPeriod: 1000
};

let client = mqtt.connect(config);

client.on('connect', () => {
    debug('Connected');
})

client.on('reconnect', () => {
    debug('Reconnecting');
})

client.on('error', (err) => {
    console.error(err);
})

client.on('disconnect', () => {
    debug('Disconnected');
})

module.exports = client;