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

file_put_contents("$LOGDIR/log.getConnection.txt", "check for session $uid2-$uid");

// check case
if (file_exists("$SESDIR/$uid2-$uid")) { // case 2
	$sessionFile = "$uid2-$uid";
	$data = file("$SESDIR/$sessionFile");
	$port2 = rtrim($data[2]);
	$port1 = rtrim($data[3]);
        $port4 = rtrim($data[5]);
        $port3 = rtrim($data[6]);
	sleep(1); // give python some time to start, see below
	print "$port1:case2:$port2:$port3:$port4";
	file_put_contents("$LOGDIR/log.getConnection.txt", "\n found existing session: $uid2-$uid, send ports: $port1/$port2 and $port3/$port4", FILE_APPEND);
} else if (file_exists("$SESDIR/$uid-$uid2")) {
	$sessionFile = "$uid-$uid2";
        $data = file("$SESDIR/$sessionFile");
        $port2 = rtrim($data[3]);
        $port1 = rtrim($data[2]);
        $port4 = rtrim($data[6]);
        $port3 = rtrim($data[5]);
        sleep(1); // give python some time to start, see below
	print "$port1:case3:$port2:$port3:$port4";
        file_put_contents("$LOGDIR/log.getConnection.txt", "\n found existing session: $uid-$uid2, send ports: $port1/$port2 and $port3/$port4", FILE_APPEND);
} else { // case 1
	// get free ports
	$port1 = findPort(4000, 4099);
	$port2 = findPort(4100, 4199);
	$port3 = findPort(4200, 4299);
	$port4 = findPort(4300, 4400);

	// create session
	$sessionFile = "$uid-$uid2";
	$now = time();
	$data = "$uid\n$uid2\n$port1\n$port2\n$now\n$port3\n$port4\n";
	file_put_contents("$SESDIR/$sessionFile", $data);

	// start TCP listeners
	$arg1 = escapeshellarg($sessionFile);
	exec("python startConnection.py $arg1 > /dev/null &"); 
	sleep(1); // wait for python to get started
	print "$port1:case1:$port2:$port3:$port4";
        file_put_contents("$LOGDIR/log.getConnection.txt", "\n created new session: $uid-$uid2, write ports: $port1/$port2 and $port3/$port4", FILE_APPEND);
}

?>
