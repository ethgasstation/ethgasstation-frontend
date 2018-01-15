<?php

/**
 * Note the database is not yet fully abstracted.
 * If you need to change DB settings, you will need to manually change
 * the files in backend/ and data_analysis to reflect these changes as
 * well, since this just fixes the PHP code.
 **/
define('DB_HOST', 'localhost');
define('DB_USERNAME', 'ethgas');
define('DB_PASSWORD', 'station');
define('DB_NAME', 'tx');
define('JSON_LOCATION', '/tmp/json');

// hostname to put in template links
define('EGS_HOSTNAME', 'localhost');
define('EGS_TITLE', 'ethgasstation-git');
define('EGS_DESCRIPTION', 'Unofficial ethgasstation.info node run by a volunteer.');

// fast dirty convenience functions
// no point in abstraction, all of this is going away
function path_to_json(string $json_file) {
    return realpath(JSON_LOCATION . '/' . $json_file);
}

function get_json_file(string $json_file_name) {
    return file_get_contents(path_to_json($json_file_name));
}