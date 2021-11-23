<?php

include 'utils.php';

$now = time();

$files = scandir($USRDIR);

$lifetime = 3*3600; // 3h, cleanup all users that are older!
$lifetime2 = 10*60; // 10 minutes when they have no sessions!

foreach ($files as &$file) {
	if ($file == ".") continue;
	if ($file == "..") continue;
	if ($file == ".keep") continue;

	$data = file("$USRDIR/$file");
	$name = rtrim($data[0]);
	$uid = rtrim($data[1]);
	$date = rtrim($data[2]);
	$refcount = rtrim($data[3]);
	$age = $now - $date;

	if ($refcount == "0") $lifetime = $lifetime2;

	if ($age > $lifetime) unlink("$USRDIR/$uid");
}

?>
