<?php

namespace Functions;

class Utils
{
    public static function print_variable($var)
    {
        //Print Variable Pretty
        echo('<pre>');
        var_dump($var);
        echo('</pre>');
    }
}

?>