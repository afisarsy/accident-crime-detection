let mysql = require('./mysql');
let mysqlFunction = require('../functions/mysqlFunction');

let User = function(user) {
    this.name = user.name,
    this.username = user.username,
    this.password = user.password
}

User.create = (newUser, result) => {
    mysql.query("INSERT INTO users " + mysqlFunction.dict2InsertQuery(newUser), (err, res) => {
        mysql.query("SELECT id FROM users WHERE " + mysqlFunction.dict2Condition(newUser), (err2, res2) => {
            if(err){
                console.error("error: ", err);
                result(err, null);
                return;
            }
            if(err2){
                console.error("error: ", err2);
            }
    
            console.log("User created: ", {id: res2[0].id, ...newUser});
            result(null, {id: res2[0].id, ...newUser});
        });
    });
};

User.findById = (userId, result) => {
    mysql.query("SELECT * FROM users WHERE id = ?", [userId], (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if (res.length) {
            console.log("User found: ", res[0]);
            result(null, res[0]);
            return;
        }

        result({ reason: "not_found" }, null);
    });
};

User.findByUserPass = (user, pass, result) => {   
    mysql.query("SELECT * FROM users WHERE " + mysqlFunction.dict2Condition({'username':user, 'password':pass}), (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if (res.length) {
            delete res[0]['password'];
            console.log("User found: ", res[0]);
            result(null, res[0]);
            return;
        }

        result({ reason: "not_found" }, null);
    });
};

User.getAll = (result) => {
    mysql.query("SELECT * FROM users", (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        console.log("Users found: ", res);
        result(null, res);
    });
};

User.updateById = (userId, newValue, result) => {
    mysql.query("UPDATE users SET " + mysqlFunction.dict2Query(newValue) + "WHERE id = ?", userId, (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if(res.affectedRows == 0){
            result({ reason: "not_found" }, null);
            return;
        }

        console.log("User updated: ", {id: userId, ...newValue});
        result(null, {id: userId, ...newValue});
    });
};

User.removeById = (userId, result) => {
    mysql.query("DELETE FROM users WHERE id = ?", [userId], (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if(res.affectedRows == 0){
            result({ reason: "not_found" }, null);
            return;
        }

        console.log("User deleted: ", res.affectedRows);
        result(null, res);
    });
};

module.exports = User;