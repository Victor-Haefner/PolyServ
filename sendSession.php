<?php

$port = $_GET['PORT'];
$msg = $_GET['MSG'];

echo file_get_contents("http://localhost:$port?MSG=$msg");

?>
