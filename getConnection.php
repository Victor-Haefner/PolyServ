<?php

include 'utils.php';

$uid = $_GET['UID'];
$uid2 = $_GET['UID2'];


// 2 cases
//  case 1: this is the first user connecting
//  case 2: this is the second user connecting

// check case
if (file_exists("$uid2-$uid")) { // case 2
	// do nothing?
} else { // case 1
	// create session
	$sessionFile = "$uid-$uid2";
	$now = time();
	$data = "$uid\n$uid2\n$now";
	file_put_contents("$SESDIR/$sessionFile", $data);
}

// open socket
ini_set("default_socket_timeout", 1); // seconds
$sock = socket_create_listen(0);
socket_set_nonblock($sock);
socket_getsockname($sock, $addr, $port);
$uri = "$addr:$port";
echo $uri;

die(extension_loaded('pcntl'));

// fork here
$pid = pcntl_fork();
if ($pid == -1) { // fork failed
	echo "fork failure!\n";
	exit();
} elseif ($pid == 0) { // child process
	include "startConnection.php";
        exit();
} else { // parent process
	exit();
}

// wait on socket
/*$timeout = 0;
$con = 0;
while($timeout < 2) {
	if (($newc = @socket_accept($sock)) !== false) {
		$con=1;
		socket_getpeername($newc, $raddr, $rport);
		print "$raddr:$rport";
	}

	if ($con==1) {
		//There is a socket. Read data from it, write data to it or close it here:
		if($dataIn = socket_read($newc, 1024)) {
			echo "Client: " . $dataIn  . "\r\n<BR>";
		}

		if ($dataIn=="") {
			socket_getpeername($newc, $raddr, $rport);
			print "$raddr:$rport";
			socket_close($newc);
			return();
		}
	}
	sleep(1);
	$timeout = $timeout+1;
}
print "\ntimer: $timeout";*/


/*$c = socket_accept($sock);
socket_getpeername($c, $raddr, $rport);
print "$raddr:$rport";*/

/*$status = socket_get_status($sock);
if ($status['timed_out']) {
	echo "socket timed out\n";
} else {
	socket_getpeername($c, $raddr, $rport);
	socket_write("hello $raddr!\n");
}*/



?>
