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

// Pobranie wiadomości z bazy danych
$query = "SELECT * FROM chat_messages ORDER BY created_at ASC";
$result = pg_query($conn, $query);

if (!$result) {
    die("Błąd zapytania: " . pg_last_error());
}

// Przechowywanie wyników w tablicy
$messages = [];
while ($row = pg_fetch_assoc($result)) {
    $messages[] = $row;
}

// Zamykanie połączenia
pg_close($conn);

// Zwrócenie wiadomości w formacie JSON
echo json_encode($messages);
?>
