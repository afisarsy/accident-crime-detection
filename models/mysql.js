let mysql = require('mysql2');
let debug = require('debug')('ACD:mysql');
debug.log = console.log.bind(console)

let config = {
    host: process.env.MYSQL_HOST || 'localhost',
    port: process.env.MYSQL_PORT || 3306,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASS,
    database: process.env.MYSQL_SCHEMA,
    connectionLimit: 10,
    queueLimit: 0,
    waitForConnections: true,
};

let pool = mysql.createPool(config);

pool.getConnection(function(err, conn) {
    if (err){
        debug("error connect to database");
        return;
    }
    debug(`connected with id ${conn.threadId}`);
    conn.release();
});

module.exports = pool;