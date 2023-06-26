<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];

if($method === 'GET') {
    echo json_encode(['message' => 'Hello, World!']);
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Not Found']);
}
?>
