<?php
require_once(__DIR__ . '/useapi.php');
run_cmd_exec("languages", $lang_list, $return_var)
?>
<h2>Submit</h2>
<form method="POST" action="/submit.php" enctype="multipart/form-data">
    <div class="uk-margin">
        <input type="hidden" name="problemId" value="<?= $problem_id ?>"> </input>
        <textarea name="usercode" , class="uk-textarea" rows="5" placeholder="Textarea"></textarea>
    </div>
    <div uk-form-custom="target: > * > span:first-child">
        <select name="lang">
            <?php
            foreach ($lang_list as $lang) {
            ?>
                <option value="<?= $lang ?>"><?= $lang ?></option>
            <?php
            }
            ?>
        </select>
        <button class="uk-button" type="button" tabindex="-1">
            <span></span>
            <span uk-icon="icon: chevron-down"></span>
        </button>
    </div>
    <button class="uk-button" type="submit">Submit</button>
</form>