module.exports.dict2Query = (dict) => {
    let query = "";
    let keys = Object.keys(dict);
    for(let i = 0; i < keys.length; i++){
        query += keys[i] + " = ";
        if(typeof dict[keys[i]] == 'string')    query += "\'" + dict[keys[i]] + "\'";
        else    query += dict[keys[i]].toString();
        if(i+1 < keys.length)   query += ","
        query += " "
    }
    return query;
}

module.exports.dict2InsertQuery = (dict) => {
    let keys = Object.keys(dict);
    let query = "(" + keys.join(',') + ") VALUES(";
    for(let i = 0; i < keys.length; i++){
        if(typeof dict[keys[i]] == 'string'){
            if(dict[keys[i]][0] == '%') query += dict[keys[i]].substring(1);
            else    query += "\'" + dict[keys[i]] + "\'";
        }
        else    query += dict[keys[i]].toString();
        if(i+1 < keys.length)   query += ","
        query += " "
    }
    query += ")";
    return query;
}

module.exports.dict2InsertSelectQuery = (dict) => {
    let keys = Object.keys(dict);
    let query = "(" + keys.join(',') + ") SELECT ";
    for(let i = 0; i < keys.length; i++){
        if(typeof dict[keys[i]] == 'string'){
            if(dict[keys[i]][0] == '%') query += dict[keys[i]].substring(1);
            else    query += "\'" + dict[keys[i]] + "\'";
        }
        else    query += dict[keys[i]].toString();
        if(i+1 < keys.length)   query += ","
        query += " "
    }
    return query;
}

module.exports.dict2Condition = (dict) => {
    let query = "";
    let keys = Object.keys(dict);
    for(let i = 0; i < keys.length; i++){
        query += keys[i] + " = ";
        if(typeof dict[keys[i]] == 'string')    query += "\'" + dict[keys[i]] + "\'";
        else    query += dict[keys[i]].toString();
        if(i+1 < keys.length)   query += " AND"
        query += " "
    }
    return query;
}