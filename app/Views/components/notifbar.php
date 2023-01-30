<?=$this->section("notifbar")?>
    <div id="notifBar" class="shadow bg-body-tertiary border border-bottom-0">
        <div id="header" class="d-flex justify-content-between px-2 py-1 border">
            <div>
                <span class="col-sm">Notification</span>
            </div>
            <div>
            <span id="totalNotif" class="col-sm">0</span>
                <i class="fa-solid fa-bell"></i>
            </div>
        </div>
        <div id="notifWrapper">
            <div id="notifContainer" class="hidden">
            </div>
        </div>
    </div>
<?=$this->endSection()?>