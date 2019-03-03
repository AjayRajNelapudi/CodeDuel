<?php
require("db.php");
$db = new CodeDuel_Database();
if (isset($_POST["submit-add"])) {
	$db->add_contestant($_POST["id-1"], $_POST["password-1"], $_POST["reg-id-1"], $_POST["name-1"], $_POST["college-1"], $_POST["year-1"]);
	$db->add_contestant($_POST["id-2"], $_POST["password-2"], $_POST["reg-id-2"], $_POST["name-2"], $_POST["college-2"], $_POST["year-2"]);
	$db->add_duel($_POST["id-1"], $_POST["id-2"]);
}

if (isset($_POST["submit-remove"])) {
	$db->remove_duel($_POST["r-id"]);
}

$contestants = $db->get_contestants();
?>

<!DOCTYPE html>
<html>
	<head>
		<title>
			Contestants
		</title>

		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>

	<body background="notebook.jpg">
		<div class="navigation-panel" align="right">
			<table rows="1" cols="3" cellspacing="10">
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

		<h2 class="contestants-banner">
    		Contestants
    	</h2>

		<table class="contestants" cols="6" cellspacing="10" cellpadding="15">
			<tr>
				<th>ID</th>
				<th>PASSWORD</th>
				<th>REG ID</th>
				<th>NAME</th>
				<th>COLLEGE</th>
				<th>YEAR</th>
				<th>DUEL ID</th>
			</tr>

			<?php
				while($row = mysqli_fetch_assoc($contestants)) {
					echo "<tr>";
          			foreach($row as $val) {
              			echo "<td>$val</td>";
          			}
          			echo "</tr>";
       			 }
			?>
		</table>

		<h3 class="contestant-banner">
			Add Contestant
		</h3>

		<form class="contestant-entry" method="POST" action="contestants.php">
			<table cols="2" cellspacing="2" cellpadding="5">
				<tr colspan="2">
					<td>
						<h4 class="contestant-banner">
							Contestant 1
						</h4>
					</td>
				</tr>

				<tr>
					<td>
						ID
					</td>
					<td>
						<input type="text" name="id-1">	
					</td>
				</tr>

				<tr>
					<td>
						PASSWORD
					</td>
					<td>
						<input type="password" name="password-1">	
					</td>
				</tr>

				<tr>
					<td>
						REG ID
					</td>
					<td>
						<input type="text" name="reg-id-1">	
					</td>
				</tr>

				<tr>
					<td>
						NAME
					</td>
					<td>
						<input type="text" name="name-1">	
					</td>
				</tr>


				<tr>
					<td>
						COLLEGE
					</td>
					<td>
						<input type="text" name="college-1">		
					</td>
				</tr>
				
				<tr>
					<td>
						YEAR
					</td>
					<td>
						<input type="text" name="year-1">
					</td>
				</tr>

				<tr colspan="2">
					<td>
						<h4 class="contestant-banner">
							Contestant 2
						</h4>
					</td>
				</tr>	
		
				<tr>
					<td>
						ID
					</td>
					<td>
						<input type="text" name="id-2">	
					</td>
				</tr>

				<tr>
					<td>
						PASSWORD
					</td>
					<td>
						<input type="password" name="password-2">	
					</td>
				</tr>

				<tr>
					<td>
						REG ID
					</td>
					<td>
						<input type="text" name="reg-id-2">	
					</td>
				</tr>

				<tr>
					<td>
						NAME
					</td>
					<td>
						<input type="text" name="name-2">	
					</td>
				</tr>


				<tr>
					<td>
						COLLEGE
					</td>
					<td>
						<input type="text" name="college-2">		
					</td>
				</tr>
				
				<tr>
					<td>
						YEAR
					</td>
					<td>
						<input type="text" name="year-2">
					</td>
				</tr>

				<tr>
					<td>
						<input type="submit" name="submit-add">
					</td>
				</tr>
			</table>
		</form>

		<h3 class="contestant-banner">
			Remove Contestant
		</h3>

		<form class="contestant-remove" method="POST" action="contestants.php">
			ID <input type="text" name="r-id">
			<input type="submit" name="submit-remove">
		</form>
	</body>
</html>