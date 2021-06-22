<?php

include 'utils.php';

$sessionFile = $argv[1];
$data = file("$SESDIR/$sessionFile");
$uri1 = rtrim($data[2]);
$uri2 = rtrim($data[3]);

file_put_contents("$LOGDIR/log.txt", "start session $sessionFile\n first client on: $uri1\n second client on: $uri2");

$uri1Params = explode(":", $uri1);
$uri2Params = explode(":", $uri2);

$sock = socket_create_listen(intval($uri1Params[1]));
$con = socket_accept($sock);

socket_getpeername($con, $raddr, $rport);
$curi = "$raddr:$rport";
file_put_contents("$LOGDIR/log.txt", "\n got connection: $curi", FILE_APPEND);

$wbytes = intval(socket_write($con, "hi!\n"));
file_put_contents("$LOGDIR/log.txt", "\n wrote $wbytes bytes", FILE_APPEND);

socket_close($sock);

$fe = intval(function_exists("pcntl"));
file_put_contents("$LOGDIR/log.txt", "\n check if function pcntl exists: $fe", FILE_APPEND);

//phpinfo();
//exit();

/*class AsyncOperation extends Thread {

    public function __construct($arg) {
        $this->arg = $arg;
    }

    public function run() {
        if ($this->arg) {
            $sleep = mt_rand(1, 10);
            printf('%s: %s  -start -sleeps %d' . "\n", date("g:i:sa"), $this->arg, $sleep);
            sleep($sleep);
            printf('%s: %s  -finish' . "\n", date("g:i:sa"), $this->arg);
        }
    }
}

// Create a array
$stack = array();

//Initiate Multiple Thread
foreach ( range("A", "D") as $i ) {
    $stack[] = new AsyncOperation($i);
}

// Start The Threads
foreach ( $stack as $t ) {
    $t->start();
}*/

//file_put_contents("$LOGDIR/log.txt", "\n  ok", FILE_APPEND);

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

?>
