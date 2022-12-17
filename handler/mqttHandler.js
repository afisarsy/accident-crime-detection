let mqtt = require('../models/mqtt');
let Location = require('./locationHandler')

mqtt.on('message', (topic, message) => {
    message = message.toString('utf-8');

    if(topic.indexOf(Location.topics['location']) != -1){
        let ownerId = topic.substring(topic.indexOf(Location.topics['location']) + 13, topic.lastIndexOf('/'));
        let id = topic.substring(topic.indexOf(ownerId) + ownerId.length + 1);
        Location.store(id, ownerId, message);
    }
})