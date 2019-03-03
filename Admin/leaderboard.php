<?php
require("db.php");
$db = new CodeDuel_Database();
$leaderboard = $db->make_leaderboard();
?>

<!DOCTYPE html>
<html>
	<head>
		<title>CodeDuel Leaderboard</title>

		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>

	<body background="notebook.jpg">
		<div class="navigation-panel" align="right">
			<table rows="1" cols="4" cellspacing="10">
				<tr>
					<td>
						<a class="navigation-button" href="contestants.php">
							Contestants
						</a>
					</td>

					<td>
						<a class="navigation-button" href="leaderboard.php">
							Leaderboard
						</a>
					</td>	

					<td>	
						<a class="navigation-button" href="about.html">
							About
						</a>
					</td>

					<td>	
						<a class="navigation-button" href="index.html">
							Logout
						</a>
					</td>			
				</tr>
			</table>
		</div>

    	<h2 class="leaderboard-banner">
    		Leaderboard
    	</h2>

		<table class="leaderboard" cols="3" cellspacing="10" cellpadding="15">
			<tr>
				<th>ID</th>
				<th>NAME</th>
				<th>DUEL ID</th>
				<th>POINTS</th>
			</tr>

			<?php
				while($row = mysqli_fetch_assoc($leaderboard)) {
					echo "<tr>";
          			foreach($row as $val) {
          				if ($val == NULL) {
          					$val = 0;
          				}
              			echo "<td>$val</td>";
          			}
          			echo "</tr>";
       			 }
			?>			
		</table>
	</body>
</html>