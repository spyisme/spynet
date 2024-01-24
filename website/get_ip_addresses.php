<?php
// Get the client's IP address
$client_ip = $_SERVER['REMOTE_ADDR'];

// Get the server's IP address
$server_ip = $_SERVER['SERVER_ADDR'];

// Display the IP addresses
echo json_encode(['client_ip' => $client_ip, 'server_ip' => $server_ip]);
?>
