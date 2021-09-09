<?php

include 'utils.php';

$uid = $_GET['UID'];
$file = "$MSGDIR/$uid";
if (file_exists($file)) {
    echo file_get_contents("$file");
    unlink("$file");
}

?>
