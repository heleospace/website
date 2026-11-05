<?php
// Issues a simple human-check sum and remembers the answer in the visitor's session.
session_start();
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$a = random_int(2, 9);
$b = random_int(1, 9);
$_SESSION['hc_answer'] = $a + $b;
$_SESSION['hc_issued'] = time();
echo json_encode(['q' => "$a + $b"]);
