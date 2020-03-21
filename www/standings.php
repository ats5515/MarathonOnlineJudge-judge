<?php
session_start();
$login_user = null;
$login_state = false;
if (isset($_SESSION["username"])) {
	$login_user = $_SESSION["username"];
	$login_state = true;
}
if (!isset($_GET["id"])) {
	header("Location: /");
	exit();
}
$problem_id = $_GET["id"];
$config_str = file_get_contents("../problems/$problem_id/config.json");
if (!$config_str) {
	header("Location: /");
	exit();
}
$config = json_decode($config_str, true);
require_once('template/useapi.php');
$standings =  json_decode(run_cmd("get_scorelist $problem_id"), true);
if (!$standings) {
	$standings = [];
}
?>
<!DOCTYPE html>
<html lang="ja">

<head>
	<?php require_once('template/head.php') ?>
	<title>Standings</title>
</head>

<body>
	<?php
	require_once('template/web_header.php');
	draw_web_header($login_state, $login_user);
	?>
	<div class="ats-container">
		<table class="ats-table">
			<tr>
				<th>Rank</th>
				<th>User</th>
				<th>Score</th>
			</tr>
			<?php
			foreach ($standings as $data) {
			?>
				<tr>
					<td><?= $data['rank'] ?></td>
					<td><?= $data['user'] ?></td>
					<td><?= $data['score'] ?></td>
				</tr>
			<?php
			}
			?>
		</table>
	</div>

</body>

</html>