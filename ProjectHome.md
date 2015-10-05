<table width='850'><tr><td align='center' valign='top'><img src='http://download.sagent.googlecode.com/git/homepage_top.png' border='0' /></td></tr><tr><td width='460' align='center' valign='top'><img src='http://download.sagent.googlecode.com/git/webapp_screenshot.png' border='0' /></td><td align='left' valign='top'><br />
Sagent is a light monitoring and notification environment consisting of two parts:<br>
<ul><li><b>engine</b> (python daemon)<br>
<ul><li>using <a href='SensorPlugins.md'>sensor plugins</a> (python scripts) to get measures<br>
</li><li>store measured values in an sqlite db<br>
</li><li>send notify, if is requested, using <a href='NotifierPlugins.md'>notifier plugins</a> (python scripts)<br>
</li><li>serve web app requests</li></ul></li></ul>

<ul><li><b>web app</b> (php) is gui of environment<br>
<ul><li>report measures of all configured sensor (update each 10 sec.)<br>
</li><li>generate graphics from ​​stored values (using <a href='http://code.google.com/p/flotr/'>flotr plotting library</a>)<br>
</li></ul></li></ul><blockquote>you can download it from <a href='Downloads.md'>downloads page</a> and follow installation instructions from <a href='Install.md'>install page</a>
</td></tr></table>
<h1>Boards</h1>
Sagent is especially suitable for using on ARM boards (low power, small size, no magnetic storage, low cost, etc.). I testing environment on <a href='http://elinux.org/RPi_Hardware'>Raspberry Pi</a> model B but it should work fine on all ARM boards that support linux, lighttpd or apache, python and php.</blockquote>


# Video #

<p align='center'><a href='http://www.youtube.com/watch?feature=player_embedded&v=UrgYXpAf6Nc' target='_blank'><img src='http://img.youtube.com/vi/UrgYXpAf6Nc/0.jpg' width='480' height=400/></p /></a>