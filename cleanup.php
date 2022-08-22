<?php

include 'utils.php';

$files = scandir($USRDIR);
foreach ($files as &$file) {
        if ($file == ".") continue;
        if ($file == "..") continue;
        if ($file == ".keep") continue;
        unlink("$USRDIR/$file");
}

$files = scandir($SESDIR);
foreach ($files as &$file) {
        if ($file == ".") continue;
        if ($file == "..") continue;
        if ($file == ".keep") continue;

	$data = file("$SESDIR/$file");
	$port = rtrim($data[7]);
	$msg = "shutdown";
	echo file_get_contents("http://localhost:$port?MSG=$msg");
}



?>
