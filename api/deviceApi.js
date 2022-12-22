var express = require('express');
var router = express.Router();
let device = require('../controllers/deviceController');
let JWT = require('../middleware/jwtAuth');

/* Get all devices */
router.get('/devices/all/', JWT.verifyToken, device.getAll);

/* Get user devices */
router.get('/devices/', JWT.verifyToken, device.getMine);

/* Register a new device */
router.post('/device/register/', JWT.verifyToken, device.register);

/* Update user device data by id */
router.put('/device/:id?', JWT.verifyToken, device.update);

/* Delete user device by id */
router.delete('/device/:id?', JWT.verifyToken, device.delete);

module.exports = router;
