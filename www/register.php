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
if (
	isset($_POST["username"]) &&
	isset($_POST["password1"]) &&
	isset($_POST["password2"])
) {

	if ($_POST["password1"] != $_POST["password2"]) {
		$register_result = false;
		$MSG = "wrong password";
	} else {
		$username = $_POST["username"];
		$password = $_POST["password1"];
		list($register_result, $MSG) = verify_register($username, $password);
		if ($register_result) {
			$_SESSION["username"] = $username;
			//$_SESSION["password"] =  password_hash($password, PASSWORD_DEFAULT);
			$MSG = "success";
			header("Location: /index.php");
			exit();
		}
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
	<title> Register </title>
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
		<form action="register.php" method="POST">
			<p>Register</p>
			<p>ユーザー名</p>
			<p class="username"><input type="text" name="username" value="<?= $init_username ?>" maxlength="32" autocomplete="OFF" /></p>
			<p>パスワード</p>
			<p class="password"><input type="password" name="password1" maxlength="32" autocomplete="OFF" /></p>
			<p>再入力</p>
			<p class="password"><input type="password" name="password2" maxlength="32" autocomplete="OFF" /></p>
			<p class="submit"><input type="submit" value="register" /></p>
		</form>
	</div>
</body>

</html>