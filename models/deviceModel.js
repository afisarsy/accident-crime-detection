let mysql = require('./mysql');
let mysqlError = require('../models/errorModel').mysqlError;
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
    var insert_device_query = `INSERT INTO devices ${mysqlFunction.dict2InsertSelectQuery(dictFunction.modifyKeys(newDevice, {owner_id: "%users.id"}))} FROM users WHERE id = '${newDevice.owner_id}'`;
    mysql.query(insert_device_query, (err, res) => {
        var get_inserted_device_id_query = `SELECT id FROM devices WHERE ${mysqlFunction.dict2Condition(newDevice)}`;
        mysql.query(get_inserted_device_id_query, (err2, res2) => {
            if(err){
                if (err.code == "ER_DUP_ENTRY"){
                    result({code: 400, type: "DEVICE_CREATE_DUPLICATE", error: "Duplicate device_id", query: insert_device_query}, null);
                    return    
                }
                result({code: 500, type: "DEVICE_CREATE", error: err, query: insert_device_query}, null);
                return;
            }
            else if(res.affectedRows < 1){                
                result({ code: 404, type: "DEVICE_CREATE_0_ROW", error: "Insert affect 0 row", query: insert_device_query}, null);
                return;
            }
            if(err2){
                result({code: 500, type: "DEVICE_GET_ID", error: err2, query: get_inserted_device_id_query}, null);
                return;
            }
    
            result(null, {id: res2[0].id, ...newDevice});
        });
    });
};

Device.getAll = (result) => {
    var get_all_devices_query = "SELECT id, device_id, owner_id, name, description, locations.doc AS last_location FROM devices LEFT JOIN locations ON devices.last_loc_id=locations._id";
    mysql.query(get_all_devices_query, (err, res) => {
        if(err){
            result({code: 500, type: "DEVICE_GET_ALL", error: err, query: get_all_devices_query}, null);
            return;
        }

        if(res.length == 0){
            result({code: 404, type: "DEVICE_GET_0_ROW", error: "No Devices found", query: get_all_devices_query}, null);
            return;
        }

        //Remove unnecessary cols from Doc
        res.forEach(row => {
            if (row.last_location != null){
                delete row.last_location['_id'];
                delete row.last_location['ownerId'];
                delete row.last_location['deviceId'];
            }
            else{
                row.last_location = "No Data"
            }
        });

        result(null, res);
    });
};

Device.findByOwnerId = (ownerId, result) => {
    var get_devices_by_owner_id_query = `SELECT id, device_id, owner_id, name, description, locations.doc AS last_location FROM devices LEFT JOIN locations ON devices.last_loc_id=locations._id WHERE owner_id = '${ownerId}'`;
    mysql.query(get_devices_by_owner_id_query, (err, res) => {
        if(err){
            result({code: 500, type: "DEVICE_GET_BY_OWNER_ID", error: err, query: get_devices_by_owner_id_query}, null);
            return;
        }

        if(res.length == 0){
            result({code: 404, type: "DEVICE_GET_BY_OWNER_ID_0_ROW", error: "No Devices found", query: get_devices_by_owner_id_query}, null);
            return;
        }

        //Remove unnecessary cols from Doc
        res.forEach(row => {
            if (row.last_location != null){
                delete row.last_location['_id'];
                delete row.last_location['ownerId'];
                delete row.last_location['deviceId'];
            }
            else{
                row.last_location = "No Data"
            }
        });
        
        result(null, res);
    });
};

Device.updateById = (id, newValue, result) => {
    var update_device_query = `UPDATE devices SET ${mysqlFunction.dict2Query(newValue)} WHERE id = '${id}'`;
    mysql.query(update_device_query, (err, res) => {
        if(err){
            if (err.code == "ER_DUP_ENTRY"){
                result({code: 400, type: "DEVICE_UPDATE_BY_ID_DUPLICATE", error: "Duplicate device_id", query: update_device_query}, null);
                return    
            }
            result({code: 500, type: "DEVICE_UPDATE_BY_ID", error: err, query: update_device_query}, null);
            return;
        }

        if(res.affectedRows == 0){
            result({code: 404, type: "DEVICE_UPDATE_BY_ID_0_ROW", error: "No Devices found", query: update_device_query}, null);
            return;
        }

        result(null, {id: id, ...newValue});
    });
};

Device.removeById = (id, result) => {
    var delete_device_query = `DELETE FROM devices WHERE id = \'${id}'`;
    mysql.query(delete_device_query, (err, res) => {
        if(err){
            result({code: 500, type: "DEVICE_DELETE_BY_ID", error: err, query: delete_device_query}, null);
            return;
        }

        if(res.affectedRows == 0){
            result({code: 404, type: "DEVICE_DELETE_BY_ID_0_ROW", error: "No Devices found", query: delete_device_query}, null);
            return;
        }

        result(null, res);
    });
};

module.exports = Device;