<?php
class CodeDuel_Database {
	private $conn = NULL;

	function __construct() {
		$servername = "localhost";
        $username = "root";
        $password = "anitscse034";
        $dbname = "CodeDuel";

        $this->conn = mysqli_connect($servername, $username, $password, $dbname);

        if (!$this->conn) {
            die("Connection failed: " . mysqli_connect_error());
        }
	}

	function print_all($result) {
        while($row = mysqli_fetch_assoc($result)){
          foreach($row as $val) {
              echo "$val ";
          }
          echo "<br>";
        }
    }

    function make_leaderboard() {
        $query = "SELECT C.c_id, C.c_name, D.duel_id,  (SELECT sum(S.points)
                                                        FROM Score S
                                                        WHERE C.c_id = S.c_id) AS Total
                    FROM Contestant C, Duel D
                    WHERE D.c_id_A = C.c_id OR D.c_id_B = C.c_id
                    ORDER BY Total DESC";
        $leaderboard = mysqli_query($this->conn, $query);
        return $leaderboard;
    }

    function validate_login($username, $password) {
        $query = "SELECT * FROM Admin WHERE admin_id = '$username' AND password = '$password'";
        $users = mysqli_query($this->conn, $query);
        if (mysqli_num_rows($users) == 1) {
          return True;
        }
        return False;
    }

    function get_contestants() {
        $query = "SELECT C.*, D.duel_id FROM Contestant C, Duel D WHERE D.c_id_A = C.c_id OR D.c_id_B = C.c_id";
        $contestants = mysqli_query($this->conn, $query);
        return $contestants;
    }

    function add_contestant($id, $password, $reg_id, $name, $college, $year) {
        $query = "  INSERT INTO Contestant
                    VALUES
                    ($id, '$password', '$reg_id', '$name', '$college', $year)";
        mysqli_query($this->conn, $query); 
    }

    function remove_duel($duel_id) {
        $query = "DELETE FROM Duel WHERE duel_id = $duel_id";
        mysqli_query($this->conn, $query);
    }

    function add_duel($id_A, $id_B) {
        $query = "INSERT INTO Duel(c_id_A, c_id_B) VALUES ($id_A, $id_B)";
        mysqli_query($this->conn, $query);
    }

	function __destruct() {
        mysqli_close($this->conn);
    }
}
?>