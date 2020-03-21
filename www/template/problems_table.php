<?php
function append_problems_header()
{
?>
	<tr>
		<th>Problem</th>
		<th>Tags</th>
		<th>Judge</th>
	</tr>
<?php
}
?>
<?php
function append_problem_config($id, $config)
{
?>

	<tr>
		<td><a href="./problem.php?id=<?= $id ?>"><?= $config["name"] ?></a></td>
		<td>
			<?php
			foreach($config["tags"] as $tag){
				echo "$tag ";
			}
			?>
		</td>
		<td>
			<?php
			if ($config["judgetype"] == "normal") {
				echo "通常";
			} else if ($config["judgetype"] == "twice") {
				echo "2回実行";
			} else if ($config["judgetype"] == "interactive") {
				echo "インタラクティブ";
			}
			?>
		</td>
	</tr>
<?php
}
?>