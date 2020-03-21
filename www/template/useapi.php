<?php 
function run_cmd($cmd){
	return shell_exec("sudo su -l ec2-user -c '" . $cmd . "'");
}

function run_cmd_exec($cmd, &$output, &$return_var){
	return exec("sudo su -l ec2-user -c '" . $cmd . "'", $output, $return_var);
}