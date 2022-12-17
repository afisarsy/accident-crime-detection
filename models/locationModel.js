let mysqlx = require('./mysqlx');
let mysqlFunction = require('../functions/mysqlFunction');
let mqtt = require('./mqtt');

module.exports.findByDeviceId = (deviceId, result, limit = 7) => {
    mysqlx.getSession()
	.then((session) => {
        let collection = session.getDefaultSchema().getCollection("locations");
		let docs = [];

        var query = collection.find("deviceId = :devId").bind("devId", deviceId).sort('_id desc').limit(limit);
		var find_location_query = {
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
				result({code: 404, type: "LOCATION_FIND_BY_DEVICE_ID_0_ROW", error: "No locations found", query: find_location_query}, null);
            	return;
			}
			
			result(null, docs);
		})
		.catch(err => {
			result({code: 500, type: "LOCATION_FIND_BY_DEVICE_ID", error: err, query: find_location_query}, null);
		})
    })
}

module.exports.store = (doc, result) => {
	mysqlx.getSession()
	.then((session) => {
		let locationId;
		session.startTransaction()
		try{
			let collection = session.getDefaultSchema().getCollection("locations");
			collection.add(doc).execute()
			.then((storeQuery) => {
				locationId = storeQuery.getGeneratedIds()[0];
				session.sql('UPDATE devices SET ' +  mysqlFunction.dict2Query({ last_loc_id: locationId }) + ' WHERE id = \'' + doc.deviceId + '\'').execute()
				.then((updateQuery) => {
					if(updateQuery.getAffectedItemsCount() < 1)	throw {message: 'Failed to update device location'};
				})
				.then(() => {
					session.commit();
					console.log('location stored with id', locationId);
					session.close();
					result(null, {id: locationId});
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

module.exports.publishLocation = (deviceId, ownerId, data) => {
	let topic = 'amw/location/' + deviceId + '/' + ownerId;
	console.log('Publishing to', topic)
	mqtt.publish(topic, JSON.stringify(data));
}