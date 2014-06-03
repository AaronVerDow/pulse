<?php
$command = $_REQUEST['command'];
$value = $_REQUEST['value'];

if (preg_match("/^[a-z_]*$/", $command)) {
    print "executing $command\n";
    if ($command == "bounce_fcserver") {
        exec("sudo /usr/local/bin/pulse-restart-fcserver");
    } elseif ($command == "bounce_peacekeeper") {
        exec("sudo /usr/local/bin/pulse-restart-peacekeeper");
    } elseif ($command == "stop_fcserver") {
        exec("sudo /usr/local/bin/pulse-stop-fcserver");
    } elseif ($command == "stop_peacekeeper") {
        exec("sudo /usr/local/bin/pulse-stop-peacekeeper");
    } elseif ($command == "stop_python") {
        exec("sudo /usr/local/bin/pulse-stop-python");
    } elseif ($command == "restart_everything") {
        exec("sudo /usr/local/bin/pulse-restart-fcserver");
        exec("sudo /usr/local/bin/pulse-restart-peacekeeper");
    } elseif ($command == "stop_everything") {
        exec("sudo /usr/local/bin/pulse-stop-fcserver");
        exec("sudo /usr/local/bin/pulse-stop-peacekeeper");
        exec("sudo /usr/local/bin/pulse-stop-python");
    } elseif ($command == "reboot") {
        exec("sudo /usr/local/bin/pulse-reboot-system");
    } else {
        exec("sudo /usr/local/bin/pulse-start-script $command.py");
    }
} else {
    print "trololololol";
}
?>
