<?php
require_once 'vendor/autoload.php'; // Composer autoload (do JWT)

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

// JWT konfiguracja
$jwt_secret = getenv('JWT_SECRET') ?: 'moj_super_tajny_klucz';
$jwt_algorithm = 'HS256';

// Sprawdzenie tokenu
$headers = getallheaders();
$auth_header = $headers['Authorization'] ?? '';

if (preg_match('/Bearer\s(\S+)/', $auth_header, $matches)) {
    $token = $matches[1];
    try {
        $decoded = JWT::decode($token, new Key($jwt_secret, $jwt_algorithm));
        $user_id = $decoded->user_id;
        $email = $decoded->email;
    } catch (Exception $e) {
        http_response_code(401);
        die(json_encode(["error" => "Nieprawidłowy token: " . $e->getMessage()]));
    }
} else {
    http_response_code(401);
    die(json_encode(["error" => "Brak tokenu."]));
}

// Po poprawnym tokenie — łączymy się z bazą:
$host = "dpg-d0bupg2dbo4c73d5fd8g-a";
$port = "5432";
$dbname = "rosliny";
$user = "admin";
$password = "hHozQDcLSRTAHbQgnU7JUJeoZG9Lricw";

$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die(json_encode(["error" => "Błąd połączenia z bazą danych: " . pg_last_error()]));
}

// Obsługa last_id (tylko nowe wiadomości)
$last_id = isset($_GET['last_id']) ? intval($_GET['last_id']) : 0;

// Pobranie wiadomości — razem z emailem użytkownika
$query = "
    SELECT cm.id, u.email, cm.message, cm.created_at
    FROM chat_messages cm
    JOIN users u ON cm.user_id = u.id
    WHERE cm.id > $last_id
    ORDER BY cm.created_at ASC
";

$result = pg_query($conn, $query);

if (!$result) {
    die(json_encode(["error" => "Błąd zapytania: " . pg_last_error()]));
}

$messages = [];
while ($row = pg_fetch_assoc($result)) {
    $messages[] = $row;
}

pg_close($conn);

// Zwracamy w JSON
header('Content-Type: application/json');
echo json_encode($messages);
?>
