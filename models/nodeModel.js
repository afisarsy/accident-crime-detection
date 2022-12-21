let mysqlx = require('./mysqlx');
let mqtt = require('./mqtt');
let mysqlFunction = require('../functions/mysqlFunction');

module.exports.findByDeviceId = (deviceId, limit, result) => {
    mysqlx.getSession()
	.then((session) => {
        let collection = session.getDefaultSchema().getCollection("node_data");
		let docs = [];

        var query = collection.find("device_id = :devId").bind("devId", deviceId).sort('timestamp desc').limit(limit);
		var find_node_data_query = {
			schema: query.getSchema().getName(),
			collection: query.getTableName(),
			criteria: query.getCriteria(),
			bindings: query.getBindings(),
			sort: query.getOrderings(),
			limit: limit
		}
		query.execute(doc => docs.push(doc))
		.then(() => {
			if(docs.length == 0) {
				result({code: 404, type: "NODE_DATA_FIND_BY_DEVICE_ID_0_ROW", error: "No data found", query: find_node_data_query}, null);
            	return;
			}
			
			result(null, docs);
		})
		.catch(err => {
			result({code: 500, type: "NODE_DATA_FIND_BY_DEVICE_ID", error: err, query: find_node_data_query}, null);
		})
    })
}

module.exports.store = (doc, result) => {
	mysqlx.getSession()
	.then((session) => {
		try{
			let collection = session.getDefaultSchema().getCollection("node_data");
			var query = collection.add(doc);
			var store_node_data_query = {
				schema: query.getSchema().getName(),
				collection: query.getTableName(),
				type: "STORE",
				doc: doc
			}
		}
		catch(err){
			session.close();

			result({type: "NODE_STORE_DATA_PREPARATION", error: err}, null);
			return;
		}
		session.startTransaction()
		query.execute()
		.then((storeQuery) => {
			let dataId = storeQuery.getGeneratedIds()[0];
			var update_device_last_data_id_query = `UPDATE devices SET ${mysqlFunction.dict2Query({ last_data_id: dataId })} WHERE ${mysqlFunction.dict2Condition({id: doc.device_id})}`;
			session.sql(update_device_last_data_id_query).execute()
			.then((res) => {
				if(res.getAffectedItemsCount() < 1){
					session.rollback();
					session.close();

					result({type: "DEVICE_UPDATE_LAST_DATA_ID_0_ROW", error: `Device ${doc.device_id} not found`, query: update_device_last_data_id_query}, null);
					return;
				}

				session.commit();
				session.close();

				result(null, {id: dataId});
			})
			.catch((err) => {
				session.rollback();
				session.close();

				result({type: "DEVICE_UPDATE_LAST_DATA_ID", error: err, query: update_device_last_data_id_query}, null);
				return;
			})
		})
		.catch((err) => {
			session.rollback();
			session.close();

			if (err.msg == "Document is missing a required field"){
				result({type: "NODE_STORE_DATA_INVALID_FIELD", error: `Missing device_id field`, query: store_node_data_query}, null);
			}

			result({type: "NODE_STORE_DATA", error: err, query: store_node_data_query}, null);
			return;
		})
	})
	.catch((err) => {
		result({type: "NODE_STORE_DATA_DB_SESSION", error: err}, null);
	})
}

module.exports.publishData = (topic, data, result) => {
	let message = JSON.stringify(data);
	mqtt.publish(topic, message, (err, res) => {
		if (err){
			result({type: "NODE_DATA_PUBLISH", error: err, message: message}, null);
			return;
		}

		result(null, res);
	})
}