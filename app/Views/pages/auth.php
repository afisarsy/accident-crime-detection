<?=$this->extend("layouts/auth")?>

<?=$this->section("styles")?>
	<?= link_tag('css/auth.css') ?>
<?=$this->endSection()?>

<?=$this->section("content")?>

	<div class="card card-outline auth-card">
		<div class="card-header text-center bg-light">
			<a href="<?= base_url('/') ?>" class="h2 card-title">Accident Crime Detection</a>
		</div>
		<div class="card-body">
			<div class="row">
				<div id="container-login" class="col <?= isset($register) ? 'hidden' : '' ?>">
					<p class="login-subtitle text-muted mb-4">Sign in to Accident Crime Detection</p>
					<form id="loginForm" action="<?= base_url('/auth/login') ?>" method="post">
						<?= csrf_field(); ?>
						<div class="input-group mb-1">
							<input id="loginUsername" type="text" name="username" class="form-control" placeholder="Username" value="<?= old('username') ?>">
							<div class="input-group-text">
								<i class="fas fa-user"></i>
							</div>
						</div>
						<span id="loginUsernameError" class="validation-text text-danger text-left mb-2"> </span>
						<div class="input-group mb-1">
							<input id="loginPassword" type="password" name="password" class="form-control" placeholder="Password" value="<?= old('password') ?>">
							<div class="input-group-text">
								<i class="fas fa-lock"></i>
							</div>
						</div>
						<span id="loginPasswordError" class="validation-text text-danger text-left mb-2"><?= isset($authentication) ? $authentication : ' '?></span>
						<div class="input-group mb-3">
							<div class="d-grid col-4 ms-auto p-0">
								<button id="btnLogin" type="button" class="btn btn-primary">Sign In</button>
							</div>
						</div>
					</form>
					<p class="mb-1">
						<a href="<?= base_url('/forgot-password') ?>">Forgot password</a>
					</p>
					<p class="mb-0">
						<a href="" class="login-form-toggle text-center">Register</a>
					</p>
				</div>
				<div id="container-register" class="col <?= isset($register) ? '' : 'hidden' ?>">
				<p class="login-subtitle text-muted mb-4">Register to Accident Crime Detection</p>
					<form id="registerForm" action="<?= base_url('/auth/register') ?>" method="post">
						<?= csrf_field(); ?>
						<div class="input-group mb-1">
							<input id="registerName" type="text" name="name" class="form-control" placeholder="Name" value="<?= old('name') ?>">
							<div class="input-group-text">
								<i class="fas fa-user"></i>
							</div>
						</div>
						<span id="registerNameError" class="validation-text text-danger text-left mb-2"> </span>
						<div class="input-group mb-1">
							<input id="registerUsername" type="text" name="username" class="form-control<?= isset($duplicateUsername) ? ' is-invalid' : ''?>" placeholder="Username" value="<?= old('username') ?>">
							<div class="input-group-text">
								<i class="fas fa-id-card"></i>
							</div>
						</div>
						<span id="registerUsernameError" class="validation-text text-danger text-left mb-2"><?= isset($duplicateUsername) ? $duplicateUsername : ' '?></span>
						<div class="input-group mb-1">
							<input id="registerPassword" type="password" name="password" class="form-control" placeholder="Password" value="<?= old('password') ?>">
							<div class="input-group-text">
								<i class="fas fa-lock"></i>
							</div>
						</div>
						<span id="registerPasswordError" class="validation-text text-danger text-left mb-2"> </span>
						<div class="input-group mb-1">
							<input id="registerCPassword" type="password" name="cpassword" class="form-control" placeholder="Confirm Password" value="<?= old('cpassword') ?>">
							<div class="input-group-text">
								<i class="fas fa-lock"></i>
							</div>
						</div>
						<span id="registerCPasswordError" class="validation-text text-danger text-left mb-2"> </span>
						<div class="input-group mb-3">
							<div class="d-grid col-4 ms-auto p-0">
								<button id="btnRegister" type="button" class="btn btn-primary">Register</button>
							</div>
						</div>
					</form>
					<p class="mb-0">
						<a href="" class="login-form-toggle text-center">Login</a>
					</p>
				</div>
			</div>
		</div>
	</div>

<?=$this->endSection()?>

<?=$this->section("scripts")?>
	<?= script_tag('js/auth.js') ?>
<?=$this->endSection()?>