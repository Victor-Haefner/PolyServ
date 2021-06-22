<?php

include 'utils.php';

$now = time();

$files = scandir($USRDIR);

foreach ($files as &$file) {
	if ($file == ".") continue;
	if ($file == "..") continue;
	if ($file == ".keep") continue;

	$data = file("$USRDIR/$file");
	print "$data[0], $data[1]; ";
}

?>
