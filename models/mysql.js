let mysql = require('mysql2');
let debug = require('debug')('app:mysql');

let config = {
    connectionLimit: 10,
    host: process.env.MYSQL_HOST || 'localhost',
    port: process.env.MYSQL_PORT || 3306,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASS,
    database: process.env.MYSQL_SCHEMA,
};

let connection = mysql.createConnection(config);

connection.connect(function(err) {
    if (err) throw err;
    debug('connected with id ' + connection.threadId);
});

module.exports = connection;