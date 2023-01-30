<?=$this->extend("layouts/dashboard")?>

<?=$this->section("styles")?>
	<?= link_tag('css/devices.css'); ?>
<?=$this->endSection()?>

<?=$this->section("content")?>
    <div id="deviceUtil" class="border-bottom shadowBottom d-flex justify-content-between container-fluid pt-2 pb-2">
        <button id="addDevice" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#modalDeviceAdd">
            <i class="fa-solid fa-square-plus"></i>
            <span>Add Device</span>
        </button>
        <input id="searchDevice" class="form-control"  type="search" placeholder="Search" aria-label="Search">
    </div>
    <div id="deviceWrapper" class="d-flex justify-content-center">
        <div id="deviceContainer" class="d-flex justify-content-start flex-wrap">
            <div class="d-flex justify-content-center loadingSpin" style="height: calc(100vh - 120px);">
                <div class="spinner-border m-auto" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        </div>
    </div>
<?=$this->endSection()?>

<?=$this->section("modal")?>
    <div id="modalDeviceAdd" class="modal fade" data-bs-keyboard="false" tabindex="-1" aria-labelledby="deviceAddLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 id="deviceAddLabel" class="modal-title fs-5">Add New Device</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="addDeviceForm">
						<?= csrf_field(); ?>
                        <div class="mb-1">
                            <label for="addDeviceId" class="form-label">ID</label>
                            <input id="addDeviceId" type="text" class="form-control" name="device_id">
						    <span id="addDeviceIdError" class="validation-text text-danger text-left mb-2"> </span>
                        </div>
                        <div class="mb-1">
                            <label for="addDeviceName" class="form-label">Name</label>
                            <input id="addDeviceName" type="text" class="form-control" name="name">
						    <span id="addDeviceNameError" class="validation-text text-danger text-left mb-2"> </span>
                        </div>
                        <div>
                            <label for="addDeviceDesc" class="form-label">Description</label>
                            <textarea id="addDeviceDesc" type="text" class="form-control" name="description"></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button id="btnDeviceAdd" type="button" class="btn btn-primary">Add</button>
                </div>
            </div>
        </div>
    </div>
    
    <div id="modalDeviceProperties" class="modal fade" data-bs-keyboard="false" tabindex="-1" aria-labelledby="devicePropertiesLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 id="devicePropertiesLabel" class="modal-title fs-5"></h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body container">
                    <div class="row">
                        <div class="col">
                            <form id="propDeviceForm">
                                <div class="mb-3">
                                    <label for="propDeviceId" class="form-label">ID</label>
                                    <input id="propDeviceId" type="text" class="form-control" name="device_id">
						            <span id="propDeviceIdError" class="validation-text text-danger text-left mb-2"> </span>
                                </div>
                                <div class="mb-3">
                                    <label for="propDeviceName" class="form-label">Name</label>
                                    <input id="propDeviceName" type="text" class="form-control" name="name">
						            <span id="propDeviceNameError" class="validation-text text-danger text-left mb-2"> </span>
                                </div>
                                <div class="">
                                    <label for="propDeviceDesc" class="form-label">Description</label>
                                    <textarea id="propDeviceDesc" type="text" class="form-control" name="description"></textarea>
                                </div>
                            </form>
                        </div>
                        <div class="d-flex flex-column col-5">
                            <label for="deviceDataContainer" class="form-label">Device Data</label>
                            <div id="deviceDataContainer" class="flex-fill">
                                <div class="d-flex justify-content-center loadingSpin">
                                    <div class="spinner-border m-auto" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button id="btnDeviceDeleteCheck" type="button" class="btn btn-danger modalTrigger" target-modal="modalDeviceDelete">Delete</button>
                    <button id="btnDeviceUpdate" type="button" class="btn btn-primary disabled">Update</button>
                </div>
            </div>
        </div>
    </div>

    <div id="modalDeviceDelete" class="modal fade" data-bs-keyboard="false" tabindex="-1" aria-labelledby="deviceDeleteLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 id="deviceDeleteLabel" class="modal-title fs-5">Confirm delete device</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <span>Delete this device?</span>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button id="btnDeviceDelete" type="button" class="btn btn-danger">Delete</button>
            </div>
            </div>
        </div>
    </div>
<?=$this->endSection()?>

<?=$this->section("scripts")?>
	<?= script_tag('js/devices.js'); ?>
<?=$this->endSection()?>