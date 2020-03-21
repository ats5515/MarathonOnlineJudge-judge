<?php
session_start();
$login_user = null;
$login_state = false;
if (isset($_SESSION["username"])) {
	$login_user = $_SESSION["username"];
	$login_state = true;
}
require_once('template/auth.php');

//check posted
$MSG = "";
if (isset($_POST["username"]) && isset($_POST["password"])) {
	$username = $_POST["username"];
	$password = $_POST["password"];
	list($login_result, $MSG) = verify_login($username, $password);
	if ($login_result) {
		$_SESSION["username"] = $username;
		//$_SESSION["password"] =  password_hash($password, PASSWORD_DEFAULT);
		header("Location: /index.php");
		exit();
	}
}
$init_username = "";
if (isset($_POST['username'])) {
	$init_username = $_POST['username'];
} else if (isset($_SESSION['username'])) {
	$init_username = $_POST['username'];
}
?>

<!DOCTYPE html>
<html lang="ja">

<head>
	<?php require_once('template/head.php') ?>
	<title> Login </title>
</head>

<body>
	<?php
	require_once('template/web_header.php');
	draw_web_header($login_state, $login_user);
	?>
	<div>
		<?php
		if (!$login_result) {
			echo "<p>$MSG</p>";
		}
		?>
	</div>

	<div class="ats-container">
		<h1>Login</h1>
		<form action="login.php" class="uk-form-horizontal" method="POST">

			<div>
				<label for="username" class="uk-form-label">username</label>
				<input type="text" class="uk-input" id="username" name="username" value="<?= $init_username ?>" maxlength="32" autocomplete="OFF" />
			</div>
			<div>
				<label for="password" class="uk-form-label">password</label>
				<input type="password" class="uk-input" id="password" name="password" maxlength="32" autocomplete="OFF" />
			</div>
			<input type="submit" class="uk-button" value="Login" />
		</form>
		<a href="register.php">register</a>
	</div>
</body>

</html>