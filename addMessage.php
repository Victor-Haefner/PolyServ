<?php

include 'utils.php';

$uid1 = $_GET['ORG'];
$uid2 = $_GET['UID'];
$msg = $_GET['MSG'];
$now = time();

$data = "\n>>>---\n$now\n$uid1\n$msg";
file_put_contents("$MSGDIR/$uid2", $data, FILE_APPEND | LOCK_EX);

?>
