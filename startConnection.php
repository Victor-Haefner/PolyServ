<?php

include 'utils.php';

//$session = $_GET['SESSION'];

// wait on socket
$timeout = 0;
$con = 0;
while($timeout < 2) {
	if (($newc = @socket_accept($sock)) !== false) {
		$con=1;
		socket_getpeername($newc, $raddr, $rport);
		print "$raddr:$rport";
	}

	/*if ($con==1) {
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
	}*/
	sleep(1);
	$timeout = $timeout+1;
}
print "\ntimer: $timeout";

?>
