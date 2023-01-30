<?=$this->section("sidebar")?>
    <div id="sideBarWrapper" class="z-1 animate">
        <nav id="sideBar" class="shadow bg-body-tertiary p-0 animate">
            <ul id="sideBarNav">
                <li id="sidebarExpand" class="navItem d-flex flex-row-reverse align-items-center" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-title="Expand" data-bs-delay='{ "show": 500, "hide": 0 }'>
                    <div class="navIcon d-flex justify-content-center align-items-center">
                        <i id="sidebarExpandIcon" class="fa-solid fa-chevron-right animate"></i>
                        <i id="sidebarShrinkIcon" class="fa-solid fa-chevron-left animate hidden"></i>
                    </div>
                    <span class="navText">Shrink</span>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li id="navMap" class="navItem d-flex flex-row-reverse align-items-center <?= $nav_title == 'Dashboard' ? 'active' : '' ?>" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-title="Map" data-bs-delay='{ "show": 500, "hide": 0 }'>
                    <div class="navIcon d-flex justify-content-center align-items-center">
                        <i class="icon fas fa-map-marked-alt"></i>
                    </div>
                    <span class="navText">Map</span>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li id="navDevices" class="navItem d-flex flex-row-reverse align-items-center <?= $nav_title == 'Devices' ? 'active' : '' ?>" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-title="Devices" data-bs-delay='{ "show": 500, "hide": 0 }'>
                    <div class="navIcon d-flex justify-content-center align-items-center">
                        <i class="fa-solid fa-microchip"></i>
                    </div>
                    <span class="navText">Devices</span>
                </li>
            </ul>
        </nav>
    </div>
<?=$this->endSection()?>