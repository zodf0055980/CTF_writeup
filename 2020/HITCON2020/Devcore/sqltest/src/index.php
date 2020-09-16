<?php
if (!isset($_REQUEST["column"]) && !isset($_REQUEST["id"])) {
    die('No input');
}

$column = $_REQUEST["column"];
$id = $_REQUEST["id"];
$sql = "select ".$column." from mytable where id ='".$id."'" ;

$conn = mysqli_connect('mysql', 'user', 'youtu.be/l11uaEjA-iI', 'sqltest');

$result = mysqli_query($conn, $sql);
if ( $result ){
    if ( mysqli_num_rows($result) > 0 ) {
        $row = mysqli_fetch_object($result);
        $str = "\$output = \$row->".$column.";";
        eval($str);
    }
} else {
    die('Database error');
}

if (isset($output)) {
    echo $output;
}
