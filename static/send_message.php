<?php
// Parametry połączenia z PostgreSQL
$host = "localhost";
$port = "5432";  // Domyślny port PostgreSQL
$dbname = "dpg-d0bupg2dbo4c73d5fd8g-a";  // Nazwa bazy danych
$user = "admin";  // Użytkownik PostgreSQL (może być inny)
$password = "hHozQDcLSRTAHbQgnU7JUJeoZG9Lricw";  // Hasło użytkownika (jeśli jest ustawione)

$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Błąd połączenia z bazą danych: " . pg_last_error());
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Pobranie wiadomości z formularza
    $message = $_POST['message'];
    $user = "Użytkownik";  // Możesz zmienić na nazwę zalogowanego użytkownika

    // Wstawienie wiadomości do bazy danych
    $query = "INSERT INTO chat_messages (message, user) VALUES ($1, $2)";
    $result = pg_query_params($conn, $query, array($message, $user));

    if (!$result) {
        die("Błąd zapytania: " . pg_last_error());
    }
}

pg_close($conn);
?>
