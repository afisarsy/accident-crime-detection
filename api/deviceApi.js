var express = require('express');
var router = express.Router();
let deviceController = require('../controllers/deviceController');

/* Get all devices */
router.get('/devices', deviceController.findAll);

/* Get devices by owner id */
router.get('/devices/:ownerId?', deviceController.findUserDevices);

/* Create a new device */
router.post('/device', deviceController.create);

/* Update device by id */
router.put('/device/:id?', deviceController.update);

/* Delete device by id */
router.delete('/device/:id?', deviceController.delete);

module.exports = router;
