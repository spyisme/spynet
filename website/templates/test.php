<?php
$serverIp = $_SERVER['SERVER_ADDR'];

echo json_encode(['ip' => $serverIp]);
?>
