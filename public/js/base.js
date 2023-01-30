$(document).ready(() => {
    //Check if element has attribute NAME
    $.fn.extend({
        hasAttr: function(name){
            var attr = $(this).attr(name);
            return (typeof attr !== 'undefined' && attr !== false);
        }
    });
});

//--------------------------------Global Functions--------------------------------
//Input regex
function inputRegex(e, regexRule) {
    switch (e.keyCode) {
        case 8:  // Backspace
        case 9:  // Tab
        case 13: // Enter
        case 37: // Left
        case 38: // Up
        case 39: // Right
        case 40: // Down
        break;
        default:
        var regex = new RegExp(regexRule);
        var key = e.key;
        if (!regex.test(key)) {
            e.preventDefault();
            return false;
        }
        break;
    }
}

//Ajax Functions
const ajaxGet = (url, data, sucessCallback, errorCallback) => {
    var csrfCookie = $.cookie('randomizer');
    $.ajax({
        url: url,
        method: 'get',
        data: data,
        success: sucessCallback,
        error: errorCallback
    });
}

const ajaxPost = (url, data, sucessCallback, errorCallback) => {
    var csrfCookie = $.cookie('randomizer');
    $.ajax({
        url: url,
        method: 'post',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        success: sucessCallback,
        error: errorCallback
    });
}

const ajaxPutDelete = (url, type, data, sucessCallback, errorCallback) => {
    var csrfCookie = $.cookie('randomizer');
    $.ajax({
        url: url,
        method: type,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            'X-CSRF-TOKEN': csrfCookie
        },
        success: sucessCallback,
        error: errorCallback
    });
}