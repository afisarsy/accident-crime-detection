var express = require('express');
var router = express.Router();
let nodeController = require('../controllers/nodeController');

/* Get node data by deviceId */
router.get('/node/:deviceId?', nodeController.findByDeviceId);

module.exports = router;
