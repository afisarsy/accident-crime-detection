<?php

namespace Functions;

class ArrayModifier
{
    public static function associative_2_indexed_array(array $associative_array, string $connector='='): array
    {
        $indexed_array = array();
        foreach($associative_array as $key => $val)
            array_push($indexed_array, $key . $connector . $val);
        return $indexed_array;
    }

    public static function array_contains_substrings(array $arr_of_str, array $arr_of_substr)
    {
        foreach($arr_of_str as $str){
            foreach($arr_of_substr as $substr){
                return str_contains($str, $substr);
            }
        }
    }
}

?>