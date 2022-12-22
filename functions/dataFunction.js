var bcrypt = require("bcrypt");

module.exports.normalizePort = (val) => {
    var port;
    if(typeof val === 'string') port = parseInt(val, 10);
    else  port = val;
  
    if (isNaN(port)) {
        // named pipe
        return val;
    }
  
    if (port >= 0) {
        // port number
        return port;
    }
  
    return false;
}

module.exports.hashPassword = (password) => {
    return bcrypt.hashSync(password, 8);
}

module.exports.checkPassword = (bodyPassword, dbPassword) => {
    return bcrypt.compareSync(bodyPassword, dbPassword);
}