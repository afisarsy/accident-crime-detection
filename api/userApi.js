let express = require('express');
let router = express.Router();
let user = require('../controllers/userController');
let JWT = require('../middleware/jwtAuth');

/* Get all users */
router.get('/users/', JWT.verifyToken, user.getAll);

/* Get user data */
router.get('/user/', JWT.verifyToken, user.getMine);

/* Login */
router.post('/login/', user.login);

/* Register a new user */
router.post('/register/', user.register);

/* Update user data */
router.put('/user/', JWT.verifyToken, user.update);

/* Delete user */
router.delete('/user/', JWT.verifyToken, user.delete);

module.exports = router;