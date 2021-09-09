<?php

include 'utils.php';

$uid = $_GET['UID'];
$msg = $_GET['MSG'];
$now = time();

$data = "\n>>>---\n$now\n$msg";
file_put_contents("$MSGDIR/$uid", $data, FILE_APPEND | LOCK_EX);

?>
