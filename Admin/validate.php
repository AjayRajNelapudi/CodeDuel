<?php
require("db.php");

$username = $_POST["username"];
$password = $_POST["password"];

$db = new CodeDuel_Database();
$login_status = $db->validate_login($username, $password);
if ($login_status) {
	header("Location: about.html");
} else {
	header("Location: error.html");
}
?>