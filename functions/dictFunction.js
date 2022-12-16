module.exports.removeKeys = (dict, keys) => {
    let data = Object.assign({}, dict);
    keys.forEach(key => {
        delete data[key];
    });
    return data;
}

module.exports.modifyKeys = (dict, keyval) => {
    let data = Object.assign({}, dict);
    let keys = Object.keys(keyval);
    keys.forEach(key => {
        if (data.hasOwnProperty(key)){
            data[key] = keyval[key];
        }
    });
    return data;
}