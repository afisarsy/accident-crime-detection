<?= doctype('html5') ?>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />

    <title>Accident Crime Detection</title>

    <!-- Bootstrap -->
    <?= link_tag('plugins/bootstrap/css/bootstrap.min.css') ?>
    
    <!-- Icons -->
    <?= link_tag('plugins/fontawesome/css/all.min.css') ?>
    
    <!-- Custom style -->
    <?= link_tag('css/base.css') ?>
    <?= link_tag('css/dashboard.css') ?>
    <?= $this->renderSection("styles"); ?>
</head>
<body>
    <?= $this->include('components/menubar'); ?>
    <?= $this->renderSection("menubar"); ?>
    
    <?= $this->include('components/sidebar'); ?>
    <?= $this->renderSection("sidebar"); ?>

    <div id="mainDashboard" class="container z-0">
        <?= $this->renderSection("content"); ?>
    </div>

    <?= $this->renderSection("modal"); ?>

    <?= $this->include('components/notifbar'); ?>
    <?= $this->renderSection("notifbar"); ?>

    <!-- JQuery -->
    <?= script_tag('plugins/jquery/jquery-3.6.0.min.js') ?>
    <?= script_tag('plugins/jquery/jquery-cookie/jquery.cookie.js') ?>
    <?= script_tag('plugins/jquery/jquery-serialize-object/jquery.serializeObject.js') ?>

    <!-- MQTT -->
    <?= script_tag('plugins/paho-mqtt/paho-mqtt-min.js') ?>

    <!-- Luxon -->
    <?= script_tag('plugins/luxon/luxon.min.js') ?>
    
    <!-- Bootstrap -->
    <?= script_tag('plugins/popper/popper.min.js') ?>
    <?= script_tag('plugins/bootstrap/js/bootstrap.min.js') ?>
    
    <!-- Custom script -->
    <?= '
        <script type="text/javascript">
        var mqttConfig = {};
        mqttConfig.host = "'. $mqtt['host'] .'";
        mqttConfig.port = '. $mqtt['port'] .';
        mqttConfig.user = "'. $mqtt['user'] .'";
        mqttConfig.pass = "'. $mqtt['pass'] .'";
        </script>
    ' ?>
    <?= script_tag('js/base.js') ?>
    <?= script_tag('js/dashboard.js') ?>
    <?= $this->renderSection("scripts"); ?>
</body>
</html>