$(document).ready(() => {
    //------------------------------------Map Init------------------------------------
    //Init leaflet
    var map = L.map('map', {
        center: initialView,
        zoom: initialZoom,
        attributionControl: false,
        zoomControl: false,
    });

    var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    L.control.zoom({
        position: 'topright'
    }).addTo(map);

    //Popup
    const generatePopupHTML = (device) => {
        popupHTML = '<p class="popupData name">' + device.name + '</p>';
        //popupHTML += '<p class="popupData id">' + device.device_id + '</p>';
        popupHTML += '<p class="popupData status' + (device.last_data.status.toLowerCase() == 'normal' ? '' : ' Alert') + '">' + device.last_data.status + '</p>';
        popupHTML += '<p class="popupData timestamp">' + device.last_data.timestamp + '</p>';

        return popupHTML;
    }

    //Icon
    var icons = {};
    icons.green = L.icon({
        iconUrl: 'green_marker_3_64.png',
        iconSize: [32, 44],
        iconAnchor: [16, 44],
        popupAnchor: [0, -44],
        shadowUrl: 'marker-shadow.png',
        shadowSize: [51, 72],
        shadowAnchor: [17, 70]
    });

    icons.red = L.icon({
        iconUrl: 'red_marker_3_64.png',
        iconSize: [32, 44],
        iconAnchor: [16, 44],
        popupAnchor: [0, -44],
        shadowUrl: 'marker-shadow.png',
        shadowSize: [51, 72],
        shadowAnchor: [17, 70]
    });

    //Marker
    var markers = {};
    const addMarker = (device) => {
        let marker = L.marker([device.last_data.lat, device.last_data.lng], {
            icon: (device.last_data.status.toLowerCase() == 'normal' ? icons.green : icons.red)
        });
        marker.bindPopup(generatePopupHTML(device));

        //MQTT data event listener
        marker.device_id = device.device_id;
        marker.device_name = device.name;
        marker.status = device.last_data.status;

        $(marker).on('mqttData', function(e, device_id, device_data){
            if(marker.status.toLowerCase() != device_data.status.toLowerCase()){
                marker.status = device_data.status;
                marker.setIcon(marker.status.toLowerCase() == 'normal' ? icons.green : icons.red);
                let deviceIndex = devices.map(device => device.device_id).indexOf(device_id)
                marker._popup.setContent(generatePopupHTML(devices[deviceIndex]));
            }
        })

        marker.addTo(map);

        markers[device.device_id] = marker;
    }

    //Centering
    const focusMap = () => {
        let locations = [];
        //locations.map(location => [location.lat, location.lng]
        devices.forEach(device => {
            if (typeof device.last_data == 'object'){
                locations.push([device.last_data.lat, device.last_data.lng]);
            }
        })   
        if (locations.length > 0){
            map.fitBounds(locations,{
                padding: [30, 30]
            });
        }
    }

    //Init Mapbox
    /*
    mapboxgl.accessToken = 'pk.eyJ1IjoiYWZpc2Fyc3kiLCJhIjoiY2t4cWtjaXg2MnAxNjJ2b2Mzc2ZlMXRxaCJ9.M_SICktIShHN_PEZRzKlcw';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11'
    });
    //*/



    //----------------------------------Device Init-----------------------------------
    //Get Devices
    const getDevices = () =>{
        ajaxGet('/devices/all', null, (response) => {
            devices = response.devices;
            devices.forEach(device => {
                if (typeof device.last_data == 'object'){
                    addMarker(device);
                }
            });
            if(initialZoom == 5){
                focusMap();
            }
        }, null);
    }
    getDevices();



    //-----------------------------------MQTT Init------------------------------------
    //On mqtt update
    const updateMap = (deviceIndex, device_id, data) => {
        if(markers.hasOwnProperty(device_id)){
            $(markers[device_id]).trigger('mqttData', [device_id, data]);
        }
        else{
            addMarker(devices[deviceIndex]);
            focusMap();
        }
    }

    //Register callback
    mqttConfig.messageListener.push(updateMap);
    
    //Connect to MQTT
    connectMQTT();
});