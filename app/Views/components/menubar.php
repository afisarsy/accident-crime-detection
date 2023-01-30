<?=$this->section("menubar")?>
	<nav id="menuBar" class="shadow navbar navbar-expand-lg bg-body-tertiary py-2 z-1 preventSelect">
        <div class="container-fluid">
            <nav id="pageLocation" style="--bs-breadcrumb-divider: url(&#34;data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 384 512'><path d='M342.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L274.7 256 105.4 86.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l192 192z' fill='%236c757d'/></svg>&#34;);" aria-label="breadcrumb">
                <ol class="breadcrumb m-auto">
                    <li class="breadcrumb-item">
                        <span>ACD</span>
                    </li>
                    <li class="breadcrumb-item">
                        <a href="/" class="<?= $nav_title == 'Dashboard' ? '' : 'hidden' ?>">Dashboard</a>
                        <a href="/devices" class="<?= $nav_title == 'Devices' ? '' : 'hidden' ?>">Devices</a>
                    </li>
                </ol>
            </nav>
            <div class="btn-group">
                <button id="userMenu" class="btn btn-primary" data-bs-toggle="dropdown" data-bs-auto-close="outside">
                    <span id="name" class="hideOverflow"><?= $user['name'] ?></span>
                    <i class="fa-solid fa-user"></i>
                </button>
                <ul id="userInfo" class="dropdown-menu dropdown-menu-lg-end animate slideInDown">
                    <li><p id="name" class="dropdown-header"><?= $user['name'] ?></p></li>
                    <li><p id="role" class="dropdown-header"><?= $user['role'] ?></p></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="user">Account</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="auth/logout">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>
<?=$this->endSection()?>