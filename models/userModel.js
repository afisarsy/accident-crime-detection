let mysql = require('./mysql');
let mysqlFunction = require('../functions/mysqlFunction');

let User = function(user) {
    this.name = user.name,
    this.username = user.username,
    this.password = user.password,
    this.role = user.role
}

User.create = (newUser, result) => {
    var insert_user_query = `INSERT INTO users ${mysqlFunction.dict2InsertQuery(newUser)}`;
    mysql.query(insert_user_query, (err, res) => {
        var get_inserted_user_id_query = `SELECT id FROM users WHERE ${mysqlFunction.dict2Condition(newUser)}`;
        mysql.query(get_inserted_user_id_query, (err2, res2) => {
            if(err){
                if (err.code == "ER_DUP_ENTRY"){
                    result({code: 400, type: "USER_CREATE_DUPLICATE", error: "Username isn't available", query: insert_user_query}, null);
                    return;
                }
                result({code: 500, type: "USER_CREATE", error: err, query: insert_user_query}, null);
                return;
            }
            if(err2){
                result({code: 500, type: "USER_GET_ID", error: err2, query: get_inserted_user_id_query}, null);
                return;
            }
    
            result(null, {id: res2[0].id, ...newUser});
        });
    });
};

User.getAll = (result) => {
    var get_all_users_query = "SELECT * FROM users";
    mysql.query(get_all_users_query, (err, res) => {
        if(err){
            result({code: 500, type: "USER_GET_ALL", error: err, query: get_all_users_query}, null);
            return;
        }

        if(res.length == 0){
            result({code: 404, type: "USER_GET_0_ROW", error: "No User found", query: get_all_users_query}, null);
            return;
        }

        result(null, res);
    });
};

User.findById = (id, result) => {
    var get_user_by_user_id_query = `SELECT id, name, username, role FROM users WHERE id = '${id}'`;
    mysql.query(get_user_by_user_id_query, (err, res) => {
        if(err){
            result({code: 500, type: "USER_GET_BY_USER_ID", error: err, query: get_user_by_user_id_query}, null);
            return;
        }

        if(res.length == 0){
            result({code: 404, type: "USER_GET_BY_USER_ID_0_ROW", error: "User not found", query: get_user_by_user_id_query}, null);
            return;
        }

        result(null, res[0]);
    });
};

User.findByUsername = (username, result) => {
    var get_user_by_username_password_query = `SELECT id, name, username, password, role FROM users WHERE ${mysqlFunction.dict2Condition({'username':username})}`;
    mysql.query(get_user_by_username_password_query, (err, res) => {
        if(err){
            result({code: 500, type: "USER_GET_BY_USERNAME", error: err, query: get_user_by_username_password_query}, null);
            return;
        }

        if(res.length == 0){
            result({code: 404, type: "USER_GET_BY_USERNAME_0_ROW", error: "Invalid Username", query: get_user_by_username_password_query}, null);
            return;
        }

        result(null, res[0]);
    });
};

User.updateById = (id, newValue, result) => {
    var update_user_query = `UPDATE users SET ${mysqlFunction.dict2Query(newValue)} WHERE id = '${id}'`;
    mysql.query(update_user_query, (err, res) => {
        if(err){
            if (err.code == "ER_DUP_ENTRY"){
                result({code: 400, type: "USER_UPDATE_BY_ID_DUPLICATE", error: "Invalid username", query: update_user_query}, null);
                return    
            }
            result({code: 500, type: "USER_UPDATE_BY_ID", error: err, query: update_user_query}, null);
            return;
        }

        if(res.affectedRows == 0){
            result({code: 404, type: "USER_UPDATE_BY_ID_0_ROW", error: "No User found", query: update_user_query}, null);
            return;
        }

        result(null, {id: id, ...newValue});
    });
};

User.removeById = (id, result) => {
    var delete_user_query = `DELETE FROM users WHERE id = '${id}'`;
    mysql.query(delete_user_query, (err, res) => {
        if(err){
            result({code: 500, type: "USER_DELETE_BY_ID", error: err, query: delete_user_query}, null);
            return;
        }

        if(res.affectedRows == 0){
            result({code: 404, type: "USER_DELETE_BY_ID_0_ROW", error: "No User found", query: delete_user_query}, null);
            return;
        }

        result(null, res);
    });
};

module.exports = User;