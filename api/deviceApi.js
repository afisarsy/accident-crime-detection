var express = require('express');
var router = express.Router();
let deviceController = require('../controllers/deviceController');

/* Get all devices */
router.get('/', deviceController.findAll);

/* Get devices by owner id */
router.get('/:ownerId', deviceController.findUserDevices);

/* Create a new device */
router.post('/', deviceController.create);

/* Update device by id */
router.put('/:id?', deviceController.update);

/* Delete device by id */
router.delete('/:id?', deviceController.delete);

module.exports = router;
