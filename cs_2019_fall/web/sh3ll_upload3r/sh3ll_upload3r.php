<h2>Sh3ll Upload3r</h2>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="my_file">
  <input type="submit" value="Upload">
</form>
<hr>
<br>
You can only upload file with this content:
<pre>
<?php echo htmlentities(file_get_contents("sh"));?>
</pre>
<hr>
<br>
<br>
<br>
<h3>Source Code:</h3>
<?php
$file = $_FILES['my_file']['tmp_name'];
$dest = 'upload/' . $_FILES['my_file']['name'];
$extension = pathinfo($_FILES['my_file']['name'],PATHINFO_EXTENSION);
$h = sha1(md5(file_get_contents($file)));

if(stripos($extension, 'h') !== FALSE) die('Bad Hacker!');

// check content
if($h === "9b651c5246040f7b776a8a81badf24382c4e1860") {
        echo "<h3 style='color:red'>OK, your shell is valid</h3>";
        move_uploaded_file($file, $dest);
} else if($file !== NULL) {
        die("Oops! You can only upload my shell :)");
}
highlight_file(__FILE__);
?>
