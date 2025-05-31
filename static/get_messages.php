<?php
// Połączenie z bazą danych
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "chat_db";  // Zmień na swoją nazwę bazy danych

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Połączenie nieudane: " . $conn->connect_error);
}

// Pobranie wiadomości z bazy danych
$result = $conn->query("SELECT * FROM chat_messages ORDER BY created_at ASC");

$messages = [];
while ($row = $result->fetch_assoc()) {
    $messages[] = $row;
}

$conn->close();

// Zwrócenie wiadomości w formacie JSON
echo json_encode($messages);
?>
