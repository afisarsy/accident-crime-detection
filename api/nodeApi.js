var express = require('express');
var router = express.Router();
let node = require('../controllers/nodeController');
let JWT = require('../middleware/jwtAuth');

/* Get node data by deviceId */
router.get('/node/:deviceId?', JWT.verifyToken, node.getData);

module.exports = router;
