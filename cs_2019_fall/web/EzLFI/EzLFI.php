<?php
highlight_file(__FILE__);
session_start();

$action = $_GET['action'];
if($action === 'register') {
    if(isset($_POST['user'])) {
        $_SESSION['user'] = $_POST['user'];
    }
} else if($action === 'module') {
    if(isset($_GET['m'])) {
        // example: m=about.php
        include("module/" . $_GET['m']);
    }
}
