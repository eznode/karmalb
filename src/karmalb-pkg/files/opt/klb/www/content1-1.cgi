###############################################################################
#
#     Karma Load Balancer CE Software License
#     This file is part of the Karma Load Balancer CE software package, a true
#     Community Edition derived from the Zen Load Balancer software package.
#     Sources available at https://github.com/sgoldthorpe/karmalb
#
#     Copyright (C) 2016 Steve Goldthorpe <dev@karmalb.org.uk>
#     Copyright (C) 2014 SOFINTEL IT ENGINEERING SL, Sevilla (Spain)
#
#     This library is free software; you can redistribute it and/or modify it
#     under the terms of the GNU Lesser General Public License as published
#     by the Free Software Foundation; either version 2.1 of the License, or
#     (at your option) any later version.
#
#     This library is distributed in the hope that it will be useful, but
#     WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#     General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this library; if not, write to the Free Software Foundation,
#     Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
###############################################################################

print "
    <!--Content INI-->
        <div id=\"page-content\">

                <!--Content Header INI-->
                        <h2>Manage::Global View</h2>
                <!--Content Header END-->";

#&help("1");
#graph
use GD::3DBarGrapher qw(creategraph);

#memory values
my @data_mem = &getMemStats();

#memory graph
$description = "img/graphs/graphmem.jpg";

&graphs( $description, @data_mem );

#load values
my @data_load = &getLoadStats();

#load graph
$description = "img/graphs/graphload.jpg";

&graphs( $description, @data_load );

#network interfaces
my @data_net = &getNetworkStats();

#network graph
$description = "img/graphs/graphnet.jpg";
&graphs( $description, @data_net );

#

####################################
# KLB COMMERCIAL INFORMATION
####################################

my $systemuuid = `/usr/sbin/dmidecode | grep UUID | awk '{print \$2}'`;
chomp ( $systemuuid );
print "<div class=\"box-header\">Karma Load Balancer Resources</div>";
print " <div class=\"box table\">
	<table class=\"commerce\">
	<thead>";
print "		<tr>";
print "			<th>Community Resources</th>";
print "		</tr>";
print "</thead>";
print "<tbody>";
print "		<tr>";

print "			<td><a href=\"https://github.com/sgoldthorpe/karmalb\">https://github.com/sgoldthorpe/karmalb</a></td>";
print "		</tr>";
print "</tbody>";
print "</table></div>";
print "<br />";

####################################
# GLOBAL FARMS INFORMATION
####################################

print "<div class=\"box-header\">Global farms information</div>";
print "	<div class=\"box table\">
	<table>
	<thead>";

@files = &getFarmList();

print "<tr>";
print "<th>Farm</th>";
print "<th>Profile</th>";
print "<th>Status</th>";
print "</tr>";
print "</thead>";
print "<tbody>";
if ( scalar ( @files ) > 0 )
{
foreach $file ( @files )
{
	print "<tr>";
	my $farmname = &getFarmName( $file );
	my $type     = &getFarmType( $farmname );

	print "<td><a href=\"index.cgi?id=1-2&action=editfarm&farmname=$farmname\">$farmname</a></td><td>$type</td>";
	$status = &getFarmStatus( $farmname );
	if ( $status ne "up" )
	{
		print "<td class=\"tc\"><img src=\"img/icons/small/stop.png\" title=\"down\" alt=\"*\" /></td>";
	}
	else
	{
		print "<td class=\"tc\"><img src=\"img/icons/small/start.png\" title=\"up\" alt=\"*\" /></td>";
	}

	print "</tr>";
}

}
else
{
	print "<tr><td colspan=\"3\">There are no farms defined.</td></tr>";
}
print "</tbody></table></div>";
print "<br />";

####################################
# MEM INFORMATION
####################################

print "<div class=\"box-header\">Memory (mb)</div>";
print " <div class=\"box table\">
        <table>
        <thead>";
print "<tr><th>$data_mem[0][0]</th><th>$data_mem[1][0]</th><th>$data_mem[2][0]</th><th>$data_mem[3][0]</th><th>$data_mem[4][0]</th><th>$data_mem[5][0]</th><th>$data_mem[6][0]</th><th>$data_mem[7][0]</th>    </tr>";
print "</thead>";

print "<tbody>";

print "<tr><td>$data_mem[0][1]</td><td>$data_mem[1][1]</td><td>$data_mem[2][1]</td><td>$data_mem[3][1]</td><td>$data_mem[4][1]</td><td>$data_mem[5][1]</td><td>$data_mem[6][1]</td><td>$data_mem[7][1]</td>    </tr>";
print "<tr style=\"background:none\;\"><td colspan=\"8\" style=\"text-align:center;\"><img src=\"img/graphs/graphmem.jpg\" alt=\"[Memory Graph]\" /></td></tr>";

print "</tbody>";
print "</table>";
print "</div>";

print "<div class=\"box-header\">Load</div>";
print " <div class=\"box table\">
        <table>
        <thead>";
print "<tr><th colspan=\"3\">Load last minute</th><th colspan=\"2\">Load Last 5 minutes</th><th colspan=\"3\">Load Last 15 minutes</th></tr>";
print "</thead>";
print "<tbody>";
print "<tr><td colspan=\"3\">$data_load[0][1]</td><td colspan=\"2\">$data_load[1][1]</td><td colspan=\"3\">$data_load[2][1]</td></tr>";
print "<tr style=\"background:none;\"><td colspan=\"8\" style=\"text-align:center;\"><img src=\"img/graphs/graphload.jpg\" alt=\"[Load Graph]\" /></td></tr>";
print "</tbody>";

print "</table>";
print "</div>";

####################################
# NETWORK TRAFFIC INFORMATION
####################################

print "\n";
print "<div class=\"box-header\">Network traffic interfaces (mb) from " . &uptime . "</div>";
print " <div class=\"box table\">
        <table>
        <thead>";
print "<tr><th>Interface</th><th>Input</th><th>Output</th></tr>";
print "</thead>";
print "<tbody>";
my $indice = @data_net;
for ( my $i = 0 ; $i < $indice - 1 ; $i = $i + 2 )
{
	my @ifname = split ( ' ', $data_net[$i][0] );
	print "<tr>";
	print "<td>$ifname[0]</td><td>$data_net[$i][1]</td><td>$data_net[$i+1][1]</td>\n";
	print "</tr>";
}

print "<tr style=\"background:none;\"><td colspan=\"3\" style=\"text-align:center;\"><img src=\"img/graphs/graphnet.jpg\" alt=\"[Network Graph\]\" /></td></tr>";

print "</tbody>";
print "</table>";
print "</div>";

print "<br class=\"cl\" /></div>\n";
