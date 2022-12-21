let express = require('express');
let router = express.Router();
let userController = require('../controllers/userController');

/* Get all users */
router.get('/users', userController.findAll);

/* Get user by id */
router.get('/user/:id?', userController.findOne);

/* Post user by auth */
router.post('/login', userController.findByAuth);

/* Create a new user */
router.post('/user/create', userController.create);

/* Update user by id */
router.put('/user/:id?', userController.update);

/* Delete user by id */
router.delete('/user/:id?', userController.delete);

module.exports = router;