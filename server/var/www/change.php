<?php
$command = $_REQUEST['command'];
$value = $_REQUEST['value'];

if (preg_match("/^[a-z_]*$/", $command)) {
    print "executing $command\n";
    if ($command == "bounce_fcserver") {
        exec("sudo /usr/local/bin/pulse-restart-fcserver");
    } elseif ($command == "bounce_peacekeeper") {
        exec("sudo /usr/local/bin/pulse-restart-peacekeeper");
    } elseif ($command == "reboot") {
        exec("sudo /usr/local/bin/pulse-reboot-system");
    } else {
        exec("sudo /usr/local/bin/pulse-start-script $command.py");
    }
} else {
    print "trololololol";
}
?>
