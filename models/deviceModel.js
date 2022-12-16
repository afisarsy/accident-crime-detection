let mysql = require('./mysql');
let mysqlFunction = require('../functions/mysqlFunction');
let dictFunction = require('../functions/dictFunction');

let Device = function(device) {
    this.device_id = device.device_id,
    this.owner_id = device.owner_id,
    this.name = device.name,
    this.description = device.description,
    this.last_loc_id = ""
}

Device.create = (newDevice, result) => {
    mysql.query("INSERT INTO devices " + mysqlFunction.dict2InsertSelectQuery(dictFunction.modifyKeys(newDevice, {owner_id: "%users.id"})) + " FROM users WHERE id = '" + newDevice.owner_id + "'", (err, res) => {
        mysql.query("SELECT id FROM devices WHERE " + mysqlFunction.dict2Condition(newDevice), (err2, res2) => {
            if(err){
                console.error("error: ", err);
                result(err, null);
                return;
            }
            else if(res.affectedRows < 1){                
                result({ reason: "not found", message: "No matching owner id" }, null);
                return;
            }
            if(err2){
                console.error("error: ", err2);
            }
    
            console.log("User created: ", {id: res2[0].id, ...newDevice});
            result(null, {id: res2[0].id, ...newDevice});
        });
    });
};

Device.findByOwnerId = (ownerId, result) => {
    mysql.query("SELECT id, device_id, owner_id, name, description, locations.doc AS data FROM devices INNER JOIN locations ON devices.last_loc_id=locations._id WHERE owner_id = ?", [ownerId], (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if (res.length) {
            console.log("Devices found: ", res);
            //Remove duplicate data from Doc
            res.forEach(row => {
                delete row.data['_id'];
                delete row.data['ownerId'];
                delete row.data['deviceId'];
            });
            result(null, res);
            return;
        }

        result({ reason: "not_found" }, null);
    });
};

Device.getAll = (result) => {
    mysql.query("SELECT id, device_id, owner_id, name, description, locations.doc AS data FROM devices INNER JOIN locations ON devices.last_loc_id=locations._id", (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        console.log("Devices found: ", res);
        //Remove duplicate data from Doc
        res.forEach(row => {
            delete row.data['_id'];
            delete row.data['ownerId'];
            delete row.data['deviceId'];
        });
        result(null, res);
    });
};

Device.updateById = (id, newValue, result) => {
    mysql.query("UPDATE devices SET " + mysqlFunction.dict2Query(newValue) + "WHERE id = ?", [id], (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if(res.affectedRows == 0){
            result({ reason: "not_found" }, null);
            return;
        }

        console.log("Device updated: ", {id: id, ...newValue});
        result(null, {id: id, ...newValue});
    });
};

Device.removeById = (id, result) => {
    mysql.query("DELETE FROM devices WHERE id = ?", [id], (err, res) => {
        if(err){
            console.error("error: ", err);
            result(err, null);
            return;
        }

        if(res.affectedRows == 0){
            result({ reason: "not_found" }, null);
            return;
        }

        console.log("Device deleted: ", res.affectedRows);
        result(null, res);
    });
};

module.exports = Device;