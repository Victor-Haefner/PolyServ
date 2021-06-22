<?php

include 'utils.php';

$uid = $_GET['UID'];
$uid2 = $_GET['UID2'];

$sessionFile = "$uid-$uid2";

$sock1 = socket_create_listen(0);
$sock2 = socket_create_listen(0);

socket_getsockname($sock1, $addr, $port);
$uri1 = "$addr:$port";

socket_getsockname($sock2, $addr, $port);
$uri2 = "$addr:$port";

while($c = socket_accept($sock)) {
   socket_getpeername($c, $raddr, $rport);
   print "Received Connection from $raddr:$rport\n";
}
socket_close($sock);

?>
