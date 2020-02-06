<?php

include("secret.php");
highlight_file(__FILE__);

class FileManager {

    public $name = '';
    public $content = '';
    public $mode = '';

    function __construct($m, $f, $c=null) {
        $this->mode = $m;
        $this->name = $f;
        $this->content = $c;
    }

    function __destruct() {
        if( $this->mode === "delete" )
            $this->delFile();
        if( $this->mode === "upload" )
            file_put_contents($this->name, $this->content);
    }

    function getFile() {
        if( $this->mode === "read" )
            return file_get_contents($this->name);
        else
            return "Bye";
    }

    function modifyFile() {
        if( $this->mode === "modify" )
            file_put_contents($this->name, $this->content);
    }

    function delFile() {
        unlink($this->name);
    }

}

$file = null;
$action = $_GET['action'];

if($action[0] === "upload") {

    $content = base64_decode($_POST['c']);
    $base = "/var/www/html/";
    $name = "uploads/" . uniqid(rand(), true);

    if( strlen($content) > 26000 ) 
        die("your img is tooooo long");
    if( substr($content, 0, 6) !== "GIF87a" && substr($content, 0, 6) !== "GIF89a" ) 
        die("GIF only!");

    $file = new FileManager("upload", $base . $name . ".gif", $content);
    echo "<img src='" . $name . ".gif'>";

} else if( $action[0] === "getsize" ) {

    $name = $_POST['f'];
    $size = getimagesize($name);
    echo "Your file size: " . $size[3];

} else if( $action[0] === "modify" ) {

    $hmac = $_GET['hmac'];
    $name = $_POST['f'];
    $content = base64_decode($_POST['c']);

    if( !is_string($hmac) || !is_string($name) || !is_string($content) ) 
        die("G__G");
    if( !hash_equals(hash_hmac("sha1", $content, $SECRET), $hmac) ) 
        die("G___G");
    if( !file_exists($name) )
        die("G____G");

    $file = new FileManager($action[0], $name, $content);
    $file->modifyFile();

} else if( $action[0] === "delete" ) {

    $hmac = $_GET['hmac'];
    $name = $_POST['f'];

    if( !is_string($hmac) || !is_string($name) ) 
        die("G__G");
    if( !hash_equals(hash_hmac("sha1", $name, $SECRET), $hmac) ) 
        die("G___G");
    if( !file_exists($name) )
        die("G____G");

    $file = new FileManager($action[0], $name);

}

