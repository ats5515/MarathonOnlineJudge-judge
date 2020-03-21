<?php
session_start();
$login_user = null;
$login_state = false;
if (isset($_SESSION["username"])) {
	$login_user = $_SESSION["username"];
	$login_state = true;
}

$problems_str = file_get_contents("../problems/problems.json");
if (!$problems_str) {
	header("Location: /");
	exit();
}
$problems = json_decode($problems_str, true);

?>
<!DOCTYPE html>
<html lang="ja">

<head>
	<?php require_once('template/head.php') ?>
	<title> Problems </title>
</head>

<body>
	<?php
	require_once('template/web_header.php');
	draw_web_header($login_state, $login_user);
	?>
	<div class="ats-container">
		<h1>Problem List</h1>
		<table class="ats-table">
			<?php
			require_once('template/problems_table.php');
			append_problems_header();
			foreach ($problems as $ID => $config) {
				append_problem_config($ID, $config);
			}
			?>
		</table>
	</div>

</body>

</html>