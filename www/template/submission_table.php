<?php
function append_header()
{
?>
	<tr>
		<th>Problem</th>
		<th>User</th>
		<th>Score</th>
		<th>Lang</th>
		<th>Status</th>
		<th>Time</th>
		<th>Memory</th>
	</tr>
<?php
}
?>
<?php
function append_submission_result($progress, $result, $info)
{
	require_once(__DIR__ . "/useapi.php");
	$prob_dir = run_cmd_exec("problems_path", $TMP, $TMP);
	$id = $info["problemId"];
	$config_str = file_get_contents("$prob_dir/$id/config.json");
	if (!$config_str) {
		header("Location: /");
		exit();
	}
	$config = json_decode($config_str, true);

?>

	<tr>
		<td><a href="/problem.php?id=<?= $info["problemId"] ?>"><?= $config["name"] ?></a></td>
		<td><?= $info["user"] ?></td>
		<td>
			<?php
			if ($progress == "done") {
				echo $result["score"];
			} else {
				echo "-";
			}
			?>
		</td>
		<td><?= $info["lang"] ?></td>
		<td>
			<span class="uk-label uk-label-success">
				<?php
				if ($progress == "done") {
					echo $result["status"];
				} else if ($progress == "WJ") {
					echo "WJ ";
				} else {
					echo $progress . "/" . $config["num_testcases"];
				}
				?>
			</span>
		</td>
		<td>
			<?php
			if ($progress == "done") {
				echo $result["time"];
			} else {
				echo "-";
			}
			?>
		</td>
		<td>
			<?php
			if ($progress == "done") {
				echo $result["memory"];
			} else {
				echo "-";
			}
			?>
		</td>
	</tr>
<?php
}
?>