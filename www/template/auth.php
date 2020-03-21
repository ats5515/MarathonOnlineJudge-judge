<?php

/**
 * 
 * string, string -> bool, string
 * 
 * $password is raw, not hashed
 * 
 * @param string $username
 * @param string $password
 * @return array(bool|string)
 *
 */
function verify_login($username, $password)
{
	if (strlen($username) > 30) {
		return [false, 'too long username'];
	}

	if (strlen($password) > 30) {
		return [false, 'too long password'];
	}

	if (!preg_match("/^[a-zA-Z0-9]+$/", $username)) {
		return [false, 'username must match "/^[a-zA-Z0-9]+$/"'];
	}

	require('template/useapi.php');
	$hash = run_cmd_exec('get_user_password ' . $username, $output, $return_var);
	if ($return_var != 0) {
		return [false, "user not registered"];
	}
	//echo "$password<br>";
	//echo "$hash<br>";
	if (!password_verify($password, $hash)) {
		return [false, "wrong password"];
	}
	return [true, ""];
}

/**
 * 
 * string, string -> bool, string
 * 
 * 
 * @param string $username
 * @param string $password
 * @return array(bool|string)
 *
 */
function verify_register($username, $password)
{


	if (strlen($username) > 30) {
		return [false, 'too long username'];
	}

	if (strlen($password) > 30) {
		return [false, 'too long password'];
	}

	if (strlen($username) <= 2 || $username == null) {
		return [false, 'username must have at least 3 chars'];
	}

	if (strlen($password) <= 2 || $password == null) {
		return [false, 'password must have  at least 3 chars'];
	}

	if (!preg_match("/^[a-zA-Z0-9]+$/", $username)) {
		return [false, 'username must match "/^[a-zA-Z0-9]+$/"'];
	}

	$hash = password_hash($password, PASSWORD_DEFAULT);
	//print($hash);
	require('template/useapi.php');
	$result = run_cmd_exec("register_user $username " . "'\\''" . $hash . "'\\''" .' 2>&1', $output, $return_var);
	if ($return_var != 0) {
		return [false, implode($output)];
	}
	return [true, ""];
}
