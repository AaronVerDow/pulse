<?php
$command = $_REQUEST['command'];
$value = $_REQUEST['value'];

if ($command == "lava") {
    exec("sudo /usr/local/bin/pulse-start-script lava_lamp.py");
    print "executing $command";
} elseif ($command == "raver") {
    exec("sudo /usr/local/bin/pulse-start-script raver_plaid.py");
    print "executing $command";
} elseif ($command == "miami") {
    exec("sudo /usr/local/bin/pulse-start-script miami.py");
    print "executing $command";
} elseif ($command == "sailor") {
    exec("sudo /usr/local/bin/pulse-start-script sailor_moon.py");
    print "executing $command";
} elseif ($command == "spatial") {
    exec("sudo /usr/local/bin/pulse-start-script spatial_stripes.py");
    print "executing $command";
} elseif ($command == "grid") {
    exec("sudo /usr/local/bin/pulse-start-script strip_count.py");
    print "executing $command";
} elseif ($command == "bounce_fcserver") {
    exec("sudo /usr/local/bin/pulse-restart-fcserver");
    print "executing $command";
} elseif ($command == "bounce_peacekeeper") {
    exec("sudo /usr/local/bin/pulse-restart-peacekeeper");
    print "executing $command";
} elseif ($command == "reboot") {
    exec("sudo /usr/local/bin/pulse-reboot-system");
} else {
    print "Nothing to do";
}
print "\n";

?>
