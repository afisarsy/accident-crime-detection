<?php

namespace Config;

// Create a new instance of our RouteCollection class.
$routes = Services::routes();

// Load the system's routing file first, so that the app and ENVIRONMENT
// can override as needed.
if (is_file(SYSTEMPATH . 'Config/Routes.php')) {
    require SYSTEMPATH . 'Config/Routes.php';
}

/*
 * --------------------------------------------------------------------
 * Router Setup
 * --------------------------------------------------------------------
 */
$routes->setDefaultNamespace('App\Controllers');
$routes->setDefaultController('Dashboard');
$routes->setDefaultMethod('index');
$routes->setTranslateURIDashes(false);
$routes->set404Override();
// The Auto Routing (Legacy) is very dangerous. It is easy to create vulnerable apps
// where controller filters or CSRF protection are bypassed.
// If you don't want to define all routes, please use the Auto Routing (Improved).
// Set `$autoRoutesImproved` to true in `app/Config/Feature.php` and set the following to true.
// $routes->setAutoRoute(false);

/*
 * --------------------------------------------------------------------
 * Route Definitions
 * --------------------------------------------------------------------
 */

// We get a performance increase by specifying the default
// route since we don't have to scan directories.
$routes->group('auth', static function($routes){
	$routes->get('/', 'Auth::index');
	$routes->post('register', 'Auth::register');
	$routes->post('login', 'Auth::login');
	$routes->get('logout', 'Auth::logout');
    $routes->get('verify', 'Auth::verify');
});
$routes->get('/', 'Dashboard::index', ['filter' => 'auth']);
$routes->group('devices', ['filter' => 'auth'], static function($routes){
	$routes->get('/', 'Dashboard::devices');
	$routes->get('all', 'Device::get_all');
});
$routes->group('device', ['filter' => 'auth'], static function($routes){
	$routes->get('(:segment)', 'Device::get_device_data/$1');
	$routes->post('add', 'Device::add');
	$routes->put('(:segment)', 'Device::update/$1');
	$routes->delete('(:segment)', 'Device::delete/$1');
});
$routes->group('user', ['filter' => 'auth'], static function($routes){
	$routes->get('/', 'User::index');
	$routes->post('update', 'User::update');
	$routes->post('delete', 'User::delete');
});
$routes->get('/notification', 'Device::get_all_device_data', ['filter' => 'auth']);

/*
 * --------------------------------------------------------------------
 * Additional Routing
 * --------------------------------------------------------------------
 *
 * There will often be times that you need additional routing and you
 * need it to be able to override any defaults in this file. Environment
 * based routes is one such time. require() additional route files here
 * to make that happen.
 *
 * You will have access to the $routes object within that file without
 * needing to reload it.
 */
if (is_file(APPPATH . 'Config/' . ENVIRONMENT . '/Routes.php')) {
    require APPPATH . 'Config/' . ENVIRONMENT . '/Routes.php';
}
