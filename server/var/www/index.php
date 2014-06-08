    <DOCTYPE html>
    <head>
<meta name="HandheldFriendly" content="true" />
<meta name="viewport" content="width=device-width, height=device-height, user-scalable=no" />
<style>
* {
    font-family: Verdana, Geneva, sans-serif;
}
body {
    background-image: url('/background.jpg');
    background-repeat: repeat;
}
p {
    padding-left: 10px;
}
ul {
    padding: 0px;
    margin: 0px;
    padding-top: 10px;
}
ul li {
    list-style-type: none;
    padding-left: 10px;
}
a:link {
    color: #9284CC;
    text-decoration: none;
}
a:hover {
    color: #9284CC;
    text-decoration: underline;
}
a:active {
    color: #9284CC;
    text-decoration: underline;
}

pre {
    background-color: black;
    color: green;
    font-weight: bold;
    font-family: "Courier New", Courier, monospace;
    padding-left: 5px;
    padding-top: 10px;
    padding-bottom: 10px;
}

h3 {
    color: #D6D6D6;
    font-weight: bold;
    padding-right: 5px;
    margin: 4px;
}
.buttons {
    text-align: center;
}
input[type="button"] {
    background-color: #3D3D3D;
    color: #D6D6D6;
    margin-top: 10px;
    margin-left: 4px;
    margin-right: 4px;
    border:none;
    font-size: 150%;
    font-weight:bold;
    width:48%;
}
.downloads {
    background-color: #B0B0B0;
}
.description {
    vertical-align: top;
    background-color: #3D3D3D;
    color: #D6D6D6;
}
.game {
    background-color: #222222;
    margin-top: 10px;
    padding: 3px;
}
.title {
    color: white;
    font-size: 150%;
    margin-left: 20px;
}
.title h1 {
    margin-bottom: 0px;
}
#status {
    color: #E26A6A;
    text-align: center;
    font-size: 130%;
    font-weight: bold;
    font-style: italic;
    padding-bottom: 10px;
    margin-top: 10px;
    margin-right: 20px;
    float: right;
}
#messages {
    color: #E26A6A;
    text-align: center;
    font-size: 150%;
    font-weight: bold;
    font-style: italic;
    padding-bottom: 10px;
    margin-top: 20px;
    margin-right: 20px;
    float: right;
    visibility: hidden;
}
.line {
    width: 100%;
    background-color: black;
}
.small_line {
    width: 100%;
    background-color: #D6D6D6;
    height: 5px;
    margin-bottom: 10px;
}
td {
}
table {
}
</style>
</head>
<script src="jquery-1.8.3.min.js"></script>
<script>
function urlParam(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}
window.blocked = false;
window.disable_blocked = false;
function disable_patterns() {
    if (window.disable_blocked == false) {
        $(".pattern").attr("disabled", "disabled");
        $(".pattern").css("color","#222222");
    }
}
function enable_patterns() {
    if (window.blocked == false) {
        $(".pattern").removeAttr("disabled");
        $(".pattern").css("color","#D6D6D6");
    }
}
function run_command(command,value) {
    disable_patterns();
	$('#messages').load("change.php", { command:command, value:value });	
    window.blocked = true;
    setTimeout(function(){window.blocked = false;enable_patterns()}, 3000);
}
function are_you_sure(command,value) {
    var r=confirm("Are you sure you want to " + command + "?");
    if (r==true) {
        run_command(command,value);
    }
}

$(document).ready(function() {
    setInterval(function() {
        $('#stats').load('index.php #stats');
    }, 1000);
    setInterval(function() {
        $('#status').load('index.php #status');
        if (/controlled by foreign host/.test($('#status').text())) {
            disable_patterns();
        } else {
            enable_patterns();
        }
    }, 1000);
    setInterval(function() {
        $('#messages').text('nothing to report');
    }, 4000);
});

</script>
<html>
<body onload=" ">
        <div id="status"><?php system("cat /tmp/fcserver.status") ?></div>
        <div class="title">
        <h1>Pulse</h1>
        </div>
        <div class="line">&nbsp;</div>

<div id="local_buttons" class="buttons">
<input id="test_button" type="button" value="Lava Lamp" class="pattern" onClick="run_command('lava_lamp');" />
<input type="button" value="Raver Plaid" class="pattern" onClick="run_command('raver_plaid');" />
<input type="button" value="Miami" class="pattern" onClick="run_command('miami');" />
<input type="button" value="Sailor Moon" class="pattern" onClick="run_command('sailor_moon');" />
<input type="button" value="Spatial Stripes" class="pattern" onClick="run_command('spatial_stripes');" />
<input type="button" value="4 Spheres" class="pattern" onClick="run_command('byb4');" />
<input type="button" value="Grid Numbers" class="pattern" onClick="run_command('strip_count');" />
<input type="button" value="White" class="pattern" onClick="run_command('white');" />
</div>

<div id="stats" class="game">
<h3>Uptime:</h3>
<pre>
<?php system("uptime"); ?>
</pre>

<h3>Network connections:</h3>
<pre>
<?php system("sudo netstat | grep fcserver"); ?>
</pre>

<h3>Processes:</h3>
<pre>
<?php system("ps -eo user -o pcpu -o etime -o args | egrep 'fcserver|pulse|_local|python' | grep -v grep"); ?>
</pre>

<h3>fcserver messages:</h3>
<pre>
<?php system("tail /var/log/fcserver.log"); ?>
</pre>

</div>
<div class="buttons">
<input type="button" value="Restart Everything" onClick="are_you_sure('restart_everything');" />
<input type="button" value="Stop Everything" onClick="are_you_sure('stop_everything');" />
<input type="button" value="Restart fcserver" onClick="are_you_sure('bounce_fcserver');" />
<input type="button" value="Stop fcserver" onClick="are_you_sure('stop_fcserver');" />
<input type="button" value="Restart Peacekeeper" onClick="are_you_sure('bounce_peacekeeper');" />
<input type="button" value="Stop Peacekeeper" onClick="are_you_sure('stop_peacekeeper');" />
<input type="button" value="Force Enable" onClick="window.disable_blocked=true;enable_patterns();" />
<input type="button" value="Stop Python" onClick="are_you_sure('stop_python');" />
<input type="button" value="Reboot" onClick="are_you_sure('reboot');" />
</div>

        <div id="messages">nothing to report</div>
</body>
