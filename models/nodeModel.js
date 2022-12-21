let mysqlx = require('./mysqlx');
let mysqlFunction = require('../functions/mysqlFunction');

module.exports.findByDeviceId = (deviceId, result, limit = 7) => {
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
		let dataId;
		session.startTransaction()
		try{
			let collection = session.getDefaultSchema().getCollection("node_data");
			var query = collection.add(doc);
			var store_node_data_query = {
				schema: query.getSchema().getName(),
				collection: query.getTableName(),
				type: "STORE",
				doc: doc
			}
			query.execute()
			.then((storeQuery) => {
				dataId = storeQuery.getGeneratedIds()[0];
				session.sql('UPDATE devices SET ' +  mysqlFunction.dict2Query({ last_loc_id: dataId }) + ' WHERE id = \'' + doc.deviceId + '\'').execute()
				.then((updateQuery) => {
					if(updateQuery.getAffectedItemsCount() < 1)	throw {message: 'Failed to store device data'};
				})
				.then(() => {
					session.commit();
					console.log('data stored with id', dataId);
					session.close();
					result(null, {id: dataId});
					return;
				})
				.catch((err) => {
					console.error("error: ", err);
					session.rollback();
					session.close();
					result(err, null);
					return;
				})
			})
			.catch((err) => {
				console.error("error: ", err);
				session.rollback();
				session.close();
				result(err, null);
				return;
			})
		}
		catch(err) {
			console.error("error: ", err);
			session.rollback();
			session.close();
			result(err, null);
			return;
		}
	})
	.catch((err) => {
		console.error("error: ", err);
		result(err, null);
	})
}