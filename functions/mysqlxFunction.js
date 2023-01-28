module.exports.array2OrQuery = (param, array) => {
    let query = '';
    for (let i = 0; i < array.length; i++){
        query += `${param} = `;
        if(typeof array[i] == 'string')    query += `'${array[i]}'`;
        else query += array[i].toString();
        if(i+1 < array.length)   query += " or ";
    }
    return query;
}