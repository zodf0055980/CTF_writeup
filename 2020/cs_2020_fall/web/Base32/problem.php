<?php
highlight_file(__FILE__);
$waf = array("&", ";", "`", ">", "cat", "flag");
foreach ($waf as $banned)
    strpos($_GET['string'], $banned) !== false && die("owo?");
?>
<pre>
<?=shell_exec('/bin/bash -c \'base32 --decode <<< "'.addslashes($_GET['string']).'"\'')?>
</pre>
