<?php

include 'utils.php';

$now = time();

$files = scandir($SESDIR);

foreach ($files as &$file) {
	if ($file == ".") continue;
	if ($file == "..") continue;
	if ($file == ".keep") continue;

	print "$SESDIR/$file\n";
}

?>
