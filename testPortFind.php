<?php

include 'utils.php';

$uid = $_GET['UID'];
$uid2 = $_GET['UID2'];

function findTCPPort($x1, $x2) {
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

function findUDPPort($x1, $x2) {
	$ports = array();

	$d = $GLOBALS['SESDIR'];
	if ($handle = opendir($d)) {
		while (false !== ($file = readdir($handle))) {
			if ('.' === $file) continue;
			if ('..' === $file) continue;

			$data = file("$d/$file");
			$p1 = $data[5];
			$p2 = $data[6];
			array_push($ports, $p1, $p2);
		}
		closedir($handle);
	}

	foreach ($ports as &$v) print " $v";

	for ($x = $x1; $x <= $x2; $x++) {
		if (!in_array($x, $ports)) {
                       	return $x;
		}
        }
        return 0;
}

	// get free ports
	$port1 = findTCPPort(4000, 4099);
	$port2 = findTCPPort(4100, 4199);
	$port3 = findUDPPort(4200, 4299);
	$port4 = findUDPPort(4300, 4400);
	$portS = findTCPPort(4401, 4500); // local service port

	print "$port1:$port2:$port3:$port4:$portS";
?>
