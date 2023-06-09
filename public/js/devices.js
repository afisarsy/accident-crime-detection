$(document).ready(function() {
    //---------------------------------HTML template----------------------------------
    const generateDeviceHTML = (device, index) => {
        var status = device.last_data.status || 'No Data';
        var timestamp = device.last_data.timestamp || '-';

        var deviceHTML = '<div id="' + device.device_id + '" class="d-flex device" data-bs-toggle="modal" data-bs-target="#modalDeviceProperties" device-index="' + index + '" device-name="' + device.name + '">';
        deviceHTML += '<div class="circle' + (status.toLowerCase() == 'normal' ? ' normal' : (status.toLowerCase() == 'car crash' || status.toLowerCase() == 'crime' ? ' Alert' : '')) + '"></div>';
        deviceHTML += '<div class="overview">';
        deviceHTML += '<p class="name">' + device.name + '</p>';
        deviceHTML += '<p class="status">' + status + '</p>';
        deviceHTML += '<p class="timestamp">' + timestamp + '</p>';
        deviceHTML += '</div>';
        deviceHTML += '</div>';

        return deviceHTML
    }

    const spinnerDeviceHTML = '<div class="d-flex justify-content-center loadingSpin" style="height: calc(100vh - 120px);"><div class="spinner-border m-auto" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    const noDeviceHTML = '<div class="d-flex justify-content-center loadingSpin" style="height: calc(100vh - 120px);"><div class="m-auto"><span>No Device Found</span></div></div>';

    const generateDeviceDataHTML = (data, index) => {
        var dataUrl = '/?lat=' + data.lat + '&lng=' + data.lng;

        var deviceDataHTML = '<div class="row deviceData">';
        deviceDataHTML += '<p class="status' + (data.status.toLowerCase() == 'normal' ? ' normal' : (data.status.toLowerCase() == 'car crash' || data.status.toLowerCase() == 'crime' ? ' Alert' : '')) + '">' + data.status + '</p>';
        deviceDataHTML += '<p class="timestamp">' + data.timestamp + '</p>';
        deviceDataHTML += '<a href="' + dataUrl + '" class="location col">Location ';
        deviceDataHTML += '<i class="fa-solid fa-arrow-up-right-from-square"></i>';
        deviceDataHTML += '</a>';
        deviceDataHTML += '</div>';

        return deviceDataHTML;
    }

    const spinnerDeviceDataHTML = '<div class="d-flex justify-content-center loadingSpin"><div class="spinner-border m-auto" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    const noDeviceDataHTML = '<div class="d-flex justify-content-center loadingSpin"><div class="m-auto"><span>No Data</span></div></div>';
    const deviceDataSeparatorHTML = '<div class="row separator"><p>|</p></div>';
    


    //----------------------------------Device Init-----------------------------------
    //Get and show device
    const getDevices = () => {
        $('#deviceDataContainer').html(spinnerDeviceHTML);
        ajaxGet('/devices/all', null, (response) => {
            devices = response.devices;
                   
                if (devices.length == 0){
                    $('#deviceContainer').html(noDeviceHTML);
                }
                else{
                    $('#deviceContainer').html('');
                    if (devices.length == 0){
                        $('#deviceDataContainer').html(noDeviceHTML);
                    }
                    else{
                        for (let i = 0; i < devices.length; i++) {
                            $('#deviceContainer').append(generateDeviceHTML(devices[i], i));
                        }
                        addSearchEvent();
                    }
                }
        }, null);
    }
    
    getDevices();

    //Search event
    const addSearchEvent = () => {
        $('.device').on('searchDevice', function(e, keyword) {
            var deviceName = $(this).attr('device-name');
            var hidden = $(this).hasClass('hidden');

            if (deviceName.includes(keyword) && hidden){
                $(this).removeClass('hidden');
            }
            else if(!deviceName.includes(keyword) && !hidden){
                $(this).addClass('hidden');
            }
        });
        $('#searchDevice').on('input', function(e) {
            $('.device').trigger('searchDevice', [$(this).val()]);
        });
    }



    //----------------------------------Modal Config----------------------------------
    //Modal button listener
    var modalTrigger = $('.modalTrigger');
    modalTrigger.click(function(e) {
        e.preventDefault();
        if(modalTrigger.hasAttr('target-modal')){
            bootstrap.Modal.getOrCreateInstance('#' + modalTrigger.attr('target-modal')).show()
        }
    });

    //Fix backdrop z-index for nested modal
    $(document).on('show.bs.modal', '.modal', function () {
        $(this).css('z-index', '');
    });
    $(document).on('shown.bs.modal', '.modal', function () {
        var zIndex = 1050 - (10 * $('.modal').length) + (10 * $('.modal.show').length);
        $(this).css('z-index', zIndex);
        $('.modal-backdrop.show').last().css('z-index', zIndex - 1);
    });

    //Input filtering
    $('#addDeviceId,#propDeviceId').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_]+$");
    })
    $('#addDeviceName,#propDeviceName').keydown(function(e) {
        inputRegex(e, "^[a-zA-Z0-9_ @#().,]+$");
    })

    //Enable update button if form modified
    const formChangeListener = () => {
        const inputChangeBehavior = () => {
            bootstrap.Modal.getOrCreateInstance('#modalDeviceProperties')._config.backdrop = 'static';
            $('#btnDeviceUpdate').removeClass('disabled');
            devicePropertyIndex = null;
        }
        $('#propDeviceId').one('change', () => {
            inputChangeBehavior();
        });
        $('#propDeviceName').one('change', () => {
            inputChangeBehavior();
        });
        $('#propDeviceDesc').one('change', () => {
            inputChangeBehavior();
        });
    }

    //Device properties modal
    var devicePropertyIndex = null;
    //Show modal init
    const exampleModal = document.getElementById('modalDeviceProperties');
    exampleModal.addEventListener('show.bs.modal', event => {
        //Button that triggered the modal
        const button = event.relatedTarget;

        const index = button.getAttribute('device-index');
        if (devicePropertyIndex != index){
            //Update the modal's content.
            bootstrap.Modal.getOrCreateInstance('#modalDeviceProperties')._config.backdrop = true;
            $('#modalDeviceProperties').attr('device-index', index);
            $('#deviceDataContainer').html(spinnerDeviceDataHTML);
            $('#btnDeviceUpdate').addClass('disabled');
            formChangeListener();

            const modalTitle = exampleModal.querySelector('.modal-title');        
            modalTitle.textContent = devices[index].device_id;
            
            const modalDeviceId = exampleModal.querySelector('.modal-body #propDeviceId');
            modalDeviceId.value = devices[index].device_id;
            $('#propDeviceId').removeClass('is-invalid');
            $('#propDeviceIdError').html(' ');

            const modalDeviceName = exampleModal.querySelector('.modal-body #propDeviceName');
            modalDeviceName.value = devices[index].name;
            $('#propDeviceName').removeClass('is-invalid');
            $('#propDeviceNameError').html(' ');

            const modalDeviceDesc = exampleModal.querySelector('.modal-body #propDeviceDesc');
            modalDeviceDesc.value = devices[index].description;

            let requestData = {
                limit: 10
            };

            //Get device location
            ajaxGet('/device/' + devices[index].device_id, requestData, (response) => {
                device_data = response.device_data;
                    
                    if (device_data.length == 0){
                        $('#deviceDataContainer').html(noDeviceDataHTML);
                    }
                    else{
                        $('#deviceDataContainer').html('');
                        for (let i = 0; i < device_data.length; i++) {
                            $('#deviceDataContainer').append(generateDeviceDataHTML(device_data[i], i));
        
                            if (i + 1 < device_data.length)
                                $('#deviceDataContainer').append(deviceDataSeparatorHTML);
                        }
                    }
            }, null);

            devicePropertyIndex = index;
        }
    });



    //-------------------------------Device Management-------------------------------
    //Add Device
    $('#btnDeviceAdd').click((e) => {
        e.preventDefault();
        var error = 0;

        var device_id = $('#addDeviceId').val();
        var name = $('#addDeviceName').val();

        if(device_id == ''){
            $('#addDeviceId').addClass('is-invalid');
            $('#addDeviceIdError').html('Device ID is required');
            error += 1;
        }
        else if(devices.filter(device => device.device_id === device_id).length > 0){
            $('#addDeviceId').addClass('is-invalid');
            $('#addDeviceIdError').html('Duplicate device ID');
            error += 1;
        }
        else{
            $('#addDeviceId').removeClass('is-invalid');
            $('#addDeviceIdError').html(' ');
        }

        if(name == ''){
            $('#addDeviceName').addClass('is-invalid');
            $('#addDeviceNameError').html('Device name is required');
            error += 1;
        }
        else if(devices.filter(device => device.name === name).length > 0){
            $('#addDeviceName').addClass('is-invalid');
            $('#addDeviceNameError').html('Duplicate device name');
            error += 1;
        }
        else{
            $('#addDeviceName').removeClass('is-invalid');
            $('#addDeviceNameError').html(' ');
        }

        if(error == 0){
            ajaxPost('/device/add', $('#addDeviceForm').serializeObject(), (response) => {
                bootstrap.Modal.getOrCreateInstance('#modalDeviceAdd').hide();
                $('#addDeviceId').val('');
                $('#addDeviceName').val('');
                $('#addDeviceDesc').val('');

                getDevices();
            }, null);
        }
    });

    //Update Device
    $('#btnDeviceUpdate').click((e) => {
        e.preventDefault();
        var error = 0;
        var index = $('#modalDeviceProperties').attr('device-index');

        var old_device_id = $('#devicePropertiesLabel').text();
        var device_id = $('#propDeviceId').val();
        var name = $('#propDeviceName').val();

        if(device_id == ''){
            $('#propDeviceId').addClass('is-invalid');
            $('#propDeviceIdError').html('Device ID is required');
            error += 1;
        }
        else if(devices.filter(device => (device.device_id === device_id && device.device_id != devices[index].device_id)).length > 0){
            $('#propDeviceId').addClass('is-invalid');
            $('#propDeviceIdError').html('Duplicate device ID');
            error += 1;
        }
        else{
            $('#propDeviceId').removeClass('is-invalid');
            $('#propDeviceIdError').html(' ');
        }

        if(name == ''){
            $('#propDeviceName').addClass('is-invalid');
            $('#propDeviceNameError').html('Device name is required');
            error += 1;
        }
        else if(devices.filter(device => (device.name === name && device.name != devices[index].name)).length > 0){
            $('#propDeviceName').addClass('is-invalid');
            $('#propDeviceNameError').html('Duplicate device name');
            error += 1;
        }
        else{
            $('#propDeviceName').removeClass('is-invalid');
            $('#propDeviceNameError').html(' ');
        }

        if(error == 0){
            ajaxPutDelete('/device/' + old_device_id, 'PUT', $('#propDeviceForm').serializeObject(), (response) => {
                bootstrap.Modal.getOrCreateInstance('#modalDeviceProperties').hide();
                
                getDevices();
            }, null);
        }
    });

    //Delete Device
    $('#btnDeviceDelete').click((e) => {
        e.preventDefault();
        var device_id = $('#devicePropertiesLabel').text();
        ajaxPutDelete('/device/' + device_id, 'DELETE', {}, (response) => {
            bootstrap.Modal.getOrCreateInstance('#modalDeviceDelete').hide();
            bootstrap.Modal.getOrCreateInstance('#modalDeviceProperties').hide();
            
            getDevices();
        }, null);
    });


    
    //-----------------------------------MQTT Init------------------------------------
    //On mqtt update
    const updateDevices = (deviceIndex, device_id, data) => {
        //Update indicator color
        if(data.status.toLowerCase() == 'normal'){
            $(`#${device_id} .circle`).removeClass('Alert');
            $(`#${device_id} .circle`).addClass('normal');
        }
        else if(data.status.toLowerCase() == 'car crash' || data.status.toLowerCase() == 'crime'){
            $(`#${device_id} .circle`).removeClass('normal');
            $(`#${device_id} .circle`).addClass('Alert');
        }

        //Update overview data
        $(`#${device_id} .overview .status`).text(data.status);
        $(`#${device_id} .overview .timestamp`).text(data.timestamp);
    }

    //Register callback
    mqttConfig.messageListener.push(updateDevices);
    
    //Connect to MQTT
    connectMQTT();
});