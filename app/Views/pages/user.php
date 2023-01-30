<?=$this->extend("layouts/basic")?>

<?=$this->section("styles")?>
	<?= link_tag('css/user.css') ?>
<?=$this->endSection()?>

<?=$this->section("content")?>
    <nav class="navbar bg-body-tertiary shadow">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fa-solid fa-angle-left"></i>
                Back
            </a>
            <span class="navbar-text">
                Account Details
            </span>
            <span class="username navbar-text">
                <?= $user['name'] ?>
            </span>
        </div>
    </nav>
    <div class="mainWindow d-flex justify-content-center">
        <div class="accountDetails d-flex align-items-center border-dark shadow">
            <form id="accountDetailForm" method="post" style="width: 100%;">
                <?= csrf_field(); ?>
                <div class="mb-1 row">
                    <label for="username" class="col-sm-2 form-label">Username</label>
                    <div class="col-sm-10">
                        <input id="username" type="text" class="form-control" name="username" value="<?= old('username') != '' ? old('username') : $user['username'] ?>">
                        <span id="usernameError" class="validation-text text-danger text-left mb-2"> </span>
                    </div>
                </div>
                <div class="mb-1 row">
                    <label for="name" class="col-sm-2 form-label">Name</label>
                    <div class="col-sm-10">
                        <input id="name" type="text" class="form-control" name="name" value="<?= old('name') ? old('name') : $user['name'] ?>">
                        <span id="nameError" class="validation-text text-danger text-left mb-2"> </span>
                    </div>
                </div>
                <div class="mb-1 row">
                    <label for="role" class="col-sm-2 form-label">Role</label>
                    <div class="col-sm-10">
                        <input id="role" type="text" class="form-control-plaintext" readonly name="role" value="<?= $user['role'] ?>">
                        <span class="validation-text text-danger text-left mb-2"> </span>
                    </div>
                </div>
                <div class="mb-1 row">
                    <label for="password" class="col-sm-2 form-label">Change Password</label>
                    <div class="col-sm-10">
                        <input id="password" type="password" class="form-control" name="password" placeholder="Not changed" value="<?= old('password') ?>">
                        <span id="passwordError" class="validation-text text-danger text-left mb-2"> </span>
                    </div>
                </div>
                <div class="mt-5 mb-2 row">
                    <label for="cpassword" class="col-sm-2 form-label">Confirm Password</label>
                    <div class="col-sm-10">
                        <input id="passwordConfirm" type="password" class="form-control <?= isset($wrongPassword) ? 'is-invalid' : '' ?>" name="cpassword">
                        <span id="cpasswordError" class="validation-text text-danger text-left mb-2"><?= isset($wrongPassword) ? 'Wrong Password' : ' ' ?></span>
                    </div>
                </div>
                <div class="text-end mb-0">
                    <button id="btnUserDeleteCheck" type="button" class="btn btn-danger ms-auto" data-bs-toggle="modal" data-bs-target="#modalUserDelete">Delete this account</button>
                    <button id="btnUserUpdate" type="button" class="btn btn-primary disabled">Update</button>
                </div>
                <div class="text-center mb-2">
                    <span id="UpdateError" class="validation-text text-danger hidden">No data changed</span>
                </div>
            </form>
        </div>
    </div>
<?=$this->endSection()?>

<?=$this->section("scripts")?>
	<?= script_tag('js/user.js') ?>
<?=$this->endSection()?>

<?=$this->section("modal")?>
    <div id="modalUserDelete" class="modal fade" data-bs-keyboard="false" tabindex="-1" aria-labelledby="deviceDeleteLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 id="userDeleteLabel" class="modal-title fs-5">Confirm delete account</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <span>Delete this account?</span>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button id="btnUserDelete" type="button" class="btn btn-danger">Delete</button>
            </div>
            </div>
        </div>
    </div>
<?=$this->endSection()?>