<?php

include 'utils.php';

$path = $_GET['PATH'];
$data = file("$path");
$port = rtrim($data[7]);
$msg = "shutdown";

echo file_get_contents("http://localhost:$port?MSG=$msg");

//unlink("$path");

?>
