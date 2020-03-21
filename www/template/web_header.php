<?php
function draw_web_header($login_state, $username)
{
?>

	<header class="ats-header">
		<div class="ats-navbar ats-navbar-left">
			<ul>
				<li><a href="./" class="ats-logo">Marathon Online Judge(β)</a></li>
				<li><a href="./problem_list.php">Problems</a></li>
				<li><a href="./user_ranking.php">Ranking</a></li>
				<li><a href="./info.php">Info</a></li>
			</ul>
		</div>
		<div class="ats-navbar ats-navbar-right">
			<ul>
				<?php
				if ($login_state) {
				?>
					<li><a href="./user.php?user=<?= $username ?>"><?= $username ?></a></li>
					<li><a href="./logout.php">Logout</a></li>
				<?php
				} else {
				?>
					<li><a href="./register.php">Register</a></li>
					<li><a href="./login.php">Login</a></li>
				<?php
				}
				?>
			</ul>
		</div>
		<div style="clear: both"></div>
	</header>
<?php
}
?>