<?php

include 'utils.php';

$uid = $_GET['UID'];
$uid2 = $_GET['UID2'];

// 2 cases
//  case 1: this is the first user connecting
//  case 2: this is the second user connecting

function findPort($x1, $x2) {
	ini_set('display_errors', '0');
	ini_set('display_startup_errors', '0');
	error_reporting(E_NONE);

	for ($x = $x1; $x <= $x2; $x++) {
		$sock = socket_create_listen($x) > null;
		if ($sock) {
			socket_close($sock);
			return $x;
		}
	}
	return 0;
}

// check case
if (file_exists("$SESDIR/$uid2-$uid")) { // case 2
	sleep(1);
	$sessionFile = "$uid2-$uid";
	$data = file("$SESDIR/$sessionFile");
	$uri1 = rtrim($data[2]);
	$uri2 = rtrim($data[3]);
	sleep(1);
	print "$uri2:case2:$uri1";
} else { // case 1
	// get free ports
	$port1 = findPort(4020, 4035);
	$port2 = findPort(4036, 4050);

	// create session
	$sessionFile = "$uid-$uid2";
	$now = time();
	$data = "$uid\n$uid2\n$port1\n$port2\n$now";
	file_put_contents("$SESDIR/$sessionFile", $data);

	// start TCP listeners
	$arg1 = escapeshellarg($sessionFile);
	exec("python startConnection.py $arg1 > /dev/null &"); 
	sleep(1);
	print "$port1:case1:$port2";
}

?>
