<?php

include 'utils.php';

$name = $_GET['NAME'];
$uid = uniqid();
$now = time();

$data = "$name\n$uid\n$now";
file_put_contents("$USRDIR/$uid", $data);

echo $uid

?>
