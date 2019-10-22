<?php

highlight_file(__FILE__);

$waf = array("&", ";", "`", "$", "|", ">");

$me0w = str_replace("..", "", $_GET['me0w']);

for($i = 0; $i < count($waf); $i++)
    if(stripos($me0w, $waf[$i]) !== FALSE) 
        die("me0w me0w!");

shell_exec("cat $me0w &> /dev/null");
