<?php

include 'utils.php';

$now = time();

$files = scandir($USRDIR);

foreach ($files as &$file) {
	if ($file == ".") continue;
	if ($file == "..") continue;
	if ($file == ".keep") continue;

	$data = file("$USRDIR/$file");
	$name = rtrim($data[0]);
	$uid = rtrim($data[1]);
	print "$name|$uid\n";
}

?>
