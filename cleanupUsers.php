<?php

include 'utils.php';

$now = time();

$files = scandir($USRDIR);

$lifetime = 3*3600; // 3h, cleanup all users that are older!

foreach ($files as &$file) {
	if ($file == ".") continue;
	if ($file == "..") continue;
	if ($file == ".keep") continue;

	$data = file("$USRDIR/$file");
	$name = rtrim($data[0]);
	$uid = rtrim($data[1]);
	$date = rtrim($data[2]);
	$age = $now - $date;

	if ($age > $lifetime) unlink("$USRDIR/$uid");
}

?>
