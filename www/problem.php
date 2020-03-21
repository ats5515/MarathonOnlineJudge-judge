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

$statement_str = file_get_contents("../problems/$problem_id/statement.md");
?>
<!DOCTYPE html>
<html lang="ja">

<head>
	<?php require_once('template/head.php') ?>
	<title> <?= $problem_id ?></title>

	<link href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.min.css" rel="stylesheet">
	<script src="https://cdn.rawgit.com/chjj/marked/master/marked.min.js"></script>
	<link href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.css" integrity="sha256-tkzDFSl16wERzhCWg0ge2tON2+D6Qe9iEaJqM4ZGd4E=" crossorigin="anonymous" type="text/css" rel="stylesheet">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.js" integrity="sha256-gNVpJCw01Tg4rruvtWJp9vS0rRchXP2YF+U+b2lp8Po=" crossorigin="anonymous" type="text/javascript"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/contrib/auto-render.min.js" integrity="sha256-ExtbCSBuYA7kq1Pz362ibde9nnsHYPt6JxuxYeZbU+c=" crossorigin="anonymous" type="text/javascript"></script>
	<script>
		document.addEventListener("DOMContentLoaded", function() {
			var md = String.raw `<?= $statement_str ?>`;
			document.getElementById("statement").innerHTML = marked(md);

			renderMathInElement(
				document.body, {
					delimiters: [{
							left: "$$",
							right: "$$",
							display: true
						},
						{
							left: "$",
							right: "$",
							display: false
						}
					],
					ignoredTags: [],
				})
		});
	</script>
</head>

<body>

	<?php
	require_once('template/web_header.php');
	draw_web_header($login_state, $login_user);
	?>

	<div class="ats-container">
		<h1><?= $config["name"] ?></h1>
		<a href="/standings.php?id=<?= $problem_id ?>">Standings</a>
	</div>
	<div id="config" class="ats-container">
		<pre><?php var_dump($config); ?></pre>
	</div>
	<div id="statement" class="markdown-body ats-container"></div>

	<div id="submit_form" class="ats-container">
		<?php
		require_once('template/submit_form.php');
		?>

	</div>
</body>

</html>