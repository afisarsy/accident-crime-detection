const MYSQL_ERROR = {
    1062: "ER_DUP_ENTRY",                       //Duplicate entry
    1452: "ER_NO_REFERENCED_ROW_2",             //No matchind foreign key
}

module.exports.mysqlError = MYSQL_ERROR;