let mysql = require('./mysql');
let mysqlError = require('../models/errorModel').mysqlError;
let mysqlFunction = require('../functions/mysqlFunction');
let dictFunction = require('../functions/dictFunction');

let Device = function(device) {
    this.device_id = device.device_id;
    this.owner_id = device.owner_id;
    this.name = device.name;
    this.description = device.description;
}

Device.create = (newDevice, result) => {
    var insert_device_ownership_query = `INSERT INTO device_ownership ${mysqlFunction.dict2InsertQuery(newDevice)}`;
    mysql.query(insert_device_ownership_query, (err, res) => {
        if(err){
            if (err.code == "ER_DUP_ENTRY"){
                result({code: 400, type: "DEVICE_CREATE_OWNERSHIP_DUPLICATE", error: "Duplicate device_id", query: insert_device_ownership_query}, null);
                return;
            }
            else if (err.code == "ER_NO_REFERENCED_ROW_2"){
                result({code: 400, type: "DEVICE_CREATE_OWNERSHIP_FOREIGN_KEY", error: "Unknown device_id or owner_id", query: insert_device_ownership_query}, null);
                return;
            }
            result({code: 500, type: "DEVICE_CREATE_OWNERSHIP", error: err, query: insert_device_ownership_query}, null);
            return;
        }

        result(null, newDevice);
    });
};

Device.getAll = (result) => {
    var get_all_devices_query = `SELECT id, (CAST(CONCAT('[', GROUP_CONCAT(CONCAT('"', ud.owner_id, '"')), ']') AS JSON)) AS owners, node_data.doc AS last_data FROM devices LEFT JOIN node_data ON devices.last_data_id=node_data._id LEFT JOIN device_ownership AS ud ON ud.device_id=id GROUP BY id`;
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
            if (row.owners == null){
                row.owners = "No Owner";
            }
            if (row.last_data == null){
                row.last_data = "No Data";
            }
        });

        result(null, res);
    });
};

Device.findByOwnerId = (ownerId, result) => {
    var get_devices_by_owner_id_query = `SELECT device_id, name, description, node_data.doc AS last_data FROM device_ownership INNER JOIN devices ON device_ownership.device_id=devices.id LEFT JOIN node_data ON devices.last_data_id=node_data._id WHERE owner_id = '${ownerId}'`;
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
            if (row.last_data != null){
                delete row.last_data['_id'];
                delete row.last_data['device_id'];
            }
            else{
                row.last_data = "No Data"
            }
        });
        
        result(null, res);
    });
};

Device.updateById = (id, ownerId, newValue, result) => {
    var update_device_query = `UPDATE device_ownership SET ${mysqlFunction.dict2Query(newValue)} WHERE ${mysqlFunction.dict2Condition({device_id: id, owner_id: ownerId})}`;
    mysql.query(update_device_query, (err, res) => {
        if(err){
            if (err.code == "ER_DUP_ENTRY"){
                result({code: 400, type: "DEVICE_UPDATE_BY_ID_DUPLICATE", error: "Duplicate device_id", query: update_device_query}, null);
                return    
            }
            else if (err.code == "ER_NO_REFERENCED_ROW_2"){
                result({code: 400, type: "DEVICE_UPDATE_OWNERSHIP_FOREIGN_KEY", error: "Unknown device_id or owner_id", query: update_device_query}, null);
                return;
            }
            result({code: 500, type: "DEVICE_UPDATE_BY_ID", error: err, query: update_device_query}, null);
            return;
        }

        if(res.affectedRows == 0){
            result({code: 404, type: "DEVICE_UPDATE_BY_ID_0_ROW", error: "No Devices found", query: update_device_query}, null);
            return;
        }

        result(null, {id: id, owner_id: ownerId, ...newValue});
    });
};

Device.removeById = (id, ownerId, result) => {
    var delete_device_query = `DELETE FROM device_ownership WHERE ${mysqlFunction.dict2Condition({device_id: id, owner_id: ownerId})}`;
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