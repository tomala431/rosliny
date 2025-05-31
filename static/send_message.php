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

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Pobranie wiadomości z formularza
    $message = $_POST['message'];
    $user = "Użytkownik";  // Możesz zmienić na nazwę zalogowanego użytkownika

    // Wstawienie wiadomości do bazy danych
    $stmt = $conn->prepare("INSERT INTO chat_messages (message, user) VALUES (?, ?)");
    $stmt->bind_param("ss", $message, $user);
    $stmt->execute();
    $stmt->close();
}

$conn->close();
?>
