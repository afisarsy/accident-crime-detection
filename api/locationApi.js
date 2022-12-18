var express = require('express');
var router = express.Router();
let locationController = require('../controllers/locationController');

/* Get location by deviceId */
router.get('/:deviceId?', locationController.findByDeviceId);

module.exports = router;
