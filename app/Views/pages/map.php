<?=$this->extend("layouts/dashboard")?>

<?=$this->section("styles")?>
    <?= '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossorigin=""/>' ?>
	<?= link_tag('css/map.css'); ?>
<?=$this->endSection()?>

<?=$this->section("content")?>
    <div id='map'></div>
<?=$this->endSection()?>

<?=$this->section("scripts")?>
    <?= '
        <script type="text/javascript">
        var initialView = ['. $map_center[0] .','. $map_center[1] .'];
        var initialZoom = '. $zoom .';
        </script>
    ' ?>
    <?= '<script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossorigin=""></script>' ?>
	<?= script_tag('js/map.js'); ?>
<?=$this->endSection()?>