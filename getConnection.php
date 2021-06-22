<?php

include 'utils.php';

$uid = $_GET['UID'];
$uid2 = $_GET['UID2'];

// 2 cases
//  case 1: this is the first user connecting
//  case 2: this is the second user connecting

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
	$sock = socket_create_listen(0);
	socket_getsockname($sock, $addr, $port);
	socket_close($sock);
	$uri1 = "$addr:$port";
	$sock = socket_create_listen(0);
	socket_getsockname($sock, $addr, $port);
	socket_close($sock);
	$uri2 = "$addr:$port";

	// create session
	$sessionFile = "$uid-$uid2";
	$now = time();
	$data = "$uid\n$uid2\n$uri1\n$uri2\n$now";
	file_put_contents("$SESDIR/$sessionFile", $data);

	// start TCP listeners
	$arg = escapeshellarg($sessionFile);
	//exec("php startConnection.php $arg > /dev/null &"); 
	exec("python startConnection.py $arg > /dev/null &"); 
	sleep(1);
	print "$uri1:case1:$uri2";
}

?>
