let express = require('express');
let router = express.Router();
let userController = require('../controllers/userController');

/* Get all users */
router.get('/', userController.findAll);

/* Get user by id */
router.get('/:id', userController.findOne);

/* Post user by auth */
router.post('/login', userController.findByAuth);

/* Create a new user */
router.post('/create', userController.create);

/* Update user by id */
router.put('/:id', userController.update);

/* Delete user by id */
router.delete('/:id', userController.delete);

module.exports = router;