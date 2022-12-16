let mysqlx = require('./mysqlx');
let mysqlFunction = require('../functions/mysqlFunction');
let mqtt = require('./mqtt');

module.exports.findByDeviceId = (deviceId, result, limit = 7) => {
    mysqlx.getSession()
	.then((session) => {
        let collection = session.getDefaultSchema().getCollection("locations");
		let docs = [];
        collection.find("deviceId = :devId").bind("devId", deviceId).sort('_id desc').limit(limit).execute(doc => docs.push(doc))
		.then(() => {
			if(docs.length) {
				console.log(docs.length,"location/s found");
				result(null, docs);
				return;
			}
			
			result(null, []);	//No location have been stored
		})
		.catch(err => {
			console.error("error: ", err);
			result(err, null);
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