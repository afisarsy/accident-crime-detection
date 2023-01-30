<?= doctype('html5') ?>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />

    <title>Welcome to Accident Crime Detection</title>

    <!-- Bootstrap -->
    <?= link_tag('plugins/bootstrap/css/bootstrap.min.css') ?>
    
    <!-- Icons -->
    <?= link_tag('plugins/fontawesome/css/all.min.css') ?>
    
    <!-- Custom style -->
    <?= link_tag('css/base.css') ?>
    <?= $this->renderSection("styles"); ?>
</head>
<body class="d-flex">
    <?= $this->renderSection("content"); ?>

    <!-- JQuery -->
    <?= script_tag('plugins/jquery/jquery-3.6.0.min.js') ?>
    <?= script_tag('plugins/jquery/jquery-cookie/jquery.cookie.js') ?>
    <?= script_tag('plugins/jquery/jquery-serialize-object/jquery.serializeObject.js') ?>
    
    <!-- Bootstrap -->
    <?= script_tag('plugins/popper/popper.min.js') ?>
    <?= script_tag('plugins/bootstrap/js/bootstrap.min.js') ?>
    
    <!-- Custom script -->
    <?= script_tag('js/base.js') ?>
    <?= $this->renderSection("scripts"); ?>
</body>
</html>