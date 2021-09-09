<?php

include 'utils.php';

$uid = $_GET['UID'];
unlink("$USRDIR/$uid");

?>
