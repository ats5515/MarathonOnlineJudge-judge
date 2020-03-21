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
$submission_id = $_GET["id"];

require_once('template/useapi.php');
$progress = run_cmd('get_progress ' . $submission_id);


$result_str = file_get_contents("../submissions/$submission_id/result.json");

if (empty($result_str)) {
	$result_str = run_cmd("get_s3_file submissions/$submission_id/result.json");
}

$result = null;
if (!empty($result_str)) {
	$result = json_decode($result_str, true);
}

$info_str = file_get_contents("../submissions/$submission_id/info.json");
if (empty($info_str)) {
	$info_str = run_cmd("get_s3_file submissions/$submission_id/info.json");
	if (empty($info_str)) {
		header("Location: /");
		exit();
	}
}

$info = json_decode($info_str, true);



$source = run_cmd("get_source_by_id $submission_id");

?>
<!DOCTYPE html>
<html lang="ja">

<head>
	<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
	<?php require_once('template/head.php') ?>
	<title>submission : <?= $submission_id ?></title>
</head>

<body>
	<?php
	require_once('template/web_header.php');
	draw_web_header($login_state, $login_user);
	?>
	<?= var_dump($progress) ?>
	<?= var_dump($result) ?>
	<?= var_dump($info) ?>
	<div class="ats-container">
		<table class="ats-table">
			<?php
			require_once('template/submission_table.php');
			append_header();
			append_submission_result($progress, $result, $info);
			?>
		</table>
	</div>
	<div class="ats-container">
		<div>
			<div id="code">
				<pre><code class="prettyprint linenums"><?= htmlspecialchars($source) ?></code></pre>
			</div>
		</div>
	</div>
</body>

</html>