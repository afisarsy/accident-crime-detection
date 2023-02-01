$(document).ready(() => {
    //Tooltip initialization
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))



    //---------------------------------HTML template----------------------------------
    const generateNotifItemHTML = (data, index) => {
        var notifItemHTML = '<div class="notifItem mb-1 border-top">';
        notifItemHTML += '<p class="name">' + (index == null ? data.name : devices[index].name) + '</p>';
        notifItemHTML += '<div class="data border">';
        notifItemHTML += '<p class="status p-1">' + data.status + '</p>';
        notifItemHTML += '</div>';
        notifItemHTML += '<p class="timestamp">' + data.timestamp + '</p>';
        notifItemHTML += '</div>';

        return notifItemHTML;
    }
    const spinnerNotifItemHTML = '<div class="d-flex justify-content-center loadingSpin notifContentTemplate"><div class="spinner-border m-auto" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    const noNotifItemHTML = '<div class="d-flex justify-content-center loadingSpin notifContentTemplate"><div class="m-auto text-center"><span>No new data<br>in the past week</span></div></div>';


    //--------------------------------Basic Functions---------------------------------
    //Include Cookies to ajax request
    $.ajaxSetup({
        xhrFields: {
           withCredentials: true
        }
    });

    //MQTT initialization
    client = new Paho.MQTT.Client(mqttConfig.host, mqttConfig.port, mqttConfig.clientId);
    client.onConnectionLost = onConnectionLost;



    //------------------------------------Sidebar-------------------------------------
    //Expand/shrink
    $('#sidebarExpand').click((e) => {
        e.preventDefault();
        if($('#sideBarWrapper').hasClass('expand')){
            $('#sideBarWrapper').removeClass('expand');
            $('#sideBarWrapper').addClass('shrink');
            
            //disable tooltips
            bootstrap.Tooltip.getInstance('#sidebarExpand').enable();
            bootstrap.Tooltip.getInstance('#navMap').enable();
            bootstrap.Tooltip.getInstance('#navDevices').enable();
        }
        else{
            $('#sideBarWrapper').addClass('expand');
            $('#sideBarWrapper').removeClass('shrink');
            
            //disable tooltips
            bootstrap.Tooltip.getInstance('#sidebarExpand').hide();
            bootstrap.Tooltip.getInstance('#sidebarExpand').disable();
            bootstrap.Tooltip.getInstance('#navMap').disable();
            bootstrap.Tooltip.getInstance('#navDevices').disable();

        }

        if(!$('#sidebarExpandIcon').hasClass('rotCCW180')){
            $('#sidebarExpandIcon').addClass('rotCCW180');
        }
        if(!$('#sidebarShrinkIcon').hasClass('rotCW180')){
            $('#sidebarShrinkIcon').addClass('rotCW180');
        }

        $('#sidebarExpandIcon').toggleClass('hidden');
        $('#sidebarShrinkIcon').toggleClass('hidden');

    });

    //Redirect to Map
    $('#navMap:not(.active)').click((e) => {
        e.preventDefault();
        window.location.href = '/';
    });

    //Redirect to Devices
    $('#navDevices:not(.active)').click((e) => {
        e.preventDefault();
        window.location.href = '/devices';
    });



    //-------------------------------Notification bar---------------------------------
    //Expand/shrink
    $('#notifBar #header').click(function(e){
        e.preventDefault();
        $('#notifBar #header').toggleClass('expanded');
        $('#notifContainer').toggleClass('hidden');
    })

    $('#notifWrapper').hover(function(e){
        $('#totalNotif').text(0);
        $('#notifBar #header').removeClass('unread');
    })

    //MQTT initialization
    const updateNotification = (deviceIndex, device_id, data) => {
        let totalUnread = parseInt($('#totalNotif').text());
        $('#totalNotif').text(totalUnread += 1);
        $('#notifBar #header').addClass('unread');

        $('#notifContainer').prepend(generateNotifItemHTML(data, deviceIndex));
    }
    mqttConfig.messageListener.push(updateNotification);

    //Get device data
    const getDeviceData = (retry) => {
        $('#notifContainer').html(spinnerNotifItemHTML);
        let requestData = {
            from: luxon.DateTime.now().minus({days: retry}).toFormat('yyyy-MM-dd 00:00:00'),
            to: luxon.DateTime.now().minus({days: retry}).toFormat('yyyy-MM-dd 23:59:59')
        };
        ajaxGet('/notification/', requestData, (response) => {
            device_data = response.device_data;
  
                if (device_data.length == 0){
                    if (retry < 7){
                        setTimeout(getDeviceData, 500, retry + 1);
                    }
                    else{
                        $('#notifContainer').html(noNotifItemHTML);
                    }
                }
                else{
                    $('#notifContainer').html('');
                    for (let i = 0; i < device_data.length; i++) {
                        $('#notifContainer').append(generateNotifItemHTML(device_data[i], null));
                    }
                }
        }, null);
    }

    getDeviceData(0);
});


//Global variable
var devices = [];
var client;
mqttConfig.clientId = $.cookie('user_id') + '_' + Math.random().toString(36).substring(2);
mqttConfig.topics = ['acd/node', 'acd/test'];
mqttConfig.messageListener = [];


//Global Functions
//MQTT Functions
function onConnect(){
    console.log('MQTT client connected');
    mqttConfig.topics.forEach(topic => {
        client.subscribe(topic + '/#', {
            onSuccess: () => {
                console.log('MQTT client subscribed to ' + topic);
            }
        });
    });
}
function onConnectionLost(responseObject){
    console.log('MQTT client disconnected');
    if (responseObject.errorCode !== 0) {
        console.log("error:"+responseObject.errorMessage);
    }
}
const connectMQTT = () => {
    client.onMessageArrived = (message) => {
        //Parse message
        let topic = message.topic;
        let payload = message.payloadString;
        
        let nodeTopic = topic.split(mqttConfig.topics[1] + '/')[1];
        let topic_params = nodeTopic.split('/');
        let device_id = topic_params[0];
        
        let data = JSON.parse(payload);

        //If user own the device
        let deviceIndex = devices.map(device => device.device_id).indexOf(device_id);
        if (deviceIndex >= 0){
            //Update device data
            devices[deviceIndex].last_data = {
                lat: data.lat,
                lng: data.lng,
                status: data.status,
                timestamp: data.timestamp
            };

            //Callback
            mqttConfig.messageListener.forEach(listener => listener(deviceIndex, device_id, data));
        }
    }

    client.connect({
        onSuccess: onConnect,
        userName: mqttConfig.user,
        password: mqttConfig.pass,
        reconnect: true
    });
}