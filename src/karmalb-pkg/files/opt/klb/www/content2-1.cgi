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
                        <h2>Monitoring::Graphs</h2>
                <!--Content Header END-->
";

#opendir(DIR, "$basedir$img_dir");
#@files = grep(/\_d.png$/,readdir(DIR));
#closedir(DIR);

# print warning if RRD graphs don't exist yet (up to 1st 5 minutes of runtime).
# still a few seconds where this page won't work, but better than nothing.
if ( !&checkRRDsExist( ) )
{
	print "Graphs have not been generated yet.  Please return later.";
}
else
{

if ( $action && $action ne "Select Graph type" )
{
	print " <div class=\"container_12\">
          <div class=\"grid_12\">
          <div class=\"box-header\"> Graphs daily, weekly, monthly yearly </div>
          <div class=\"box stats\">
	";
	print '<div class="tc"><img src="data:image/png;base64,' . &printGraph( $action, "d" ) . '" alt="[Daily Graph]" /></div><br /><br />';
	print '<div class="tc"><img src="data:image/png;base64,' . &printGraph( $action, "w" ) . '" alt="[Weekly Graph]" /></div><br /><br />';
	print '<div class="tc"><img src="data:image/png;base64,' . &printGraph( $action, "m" ) . '" alt="[Monthly Graph]" /></div><br /><br />';
	print '<div class="tc"><img src="data:image/png;base64,' . &printGraph( $action, "y" ) . '" alt="[Yearly Graph]" /></div><br /><br />';

	print "</div></div></div>";
	print "<form method=\"get\" action=\"index.cgi\">";
	print "<input type=\"hidden\" name=\"id\" value=\"2-1\" />";
	print "<input type=\"submit\" value=\"Return\" name=\"return\" class=\"button small\" />";
	print "</form>";
}
else
{
	if ( $graphtype eq "System" )
	{
		@graphselected[0] = "";
		@graphselected[1] = "selected=\"selected\"";
		@graphselected[2] = "";
		@graphselected[3] = "";
	}
	elsif ( $graphtype eq "Network" )
	{
		@graphselected[0] = "";
		@graphselected[1] = "";
		@graphselected[2] = "selected=\"selected\"";
		@graphselected[3] = "";
	}
	elsif ( $graphtype eq "Farm" )
	{
		@graphselected[0] = "";
		@graphselected[1] = "";
		@graphselected[2] = "";
		@graphselected[3] = "selected=\"selected\"";
	}
	else
	{
		@graphselected[0] = "";
		@graphselected[1] = "";
		@graphselected[2] = "";
		@graphselected[3] = "";
	}
	print " <div class=\"container_12\">
          <div class=\"grid_12\">
          <div class=\"box-header\"> $graphtype Graphs daily </div>
          <div class=\"box stats\">
	";
	print "<form method=\"get\" action=\"index.cgi\">";
	print "<b>Select the type of Graphs to show</b>";
	print "<br />";
	print "<select name=\"graphtype\">\n";
	print "<option value=\"All\" @graphselected[0]>Show all Graphs</option>";
	print "<option value=\"System\" @graphselected[1]>Show system type Graphs</option>";
	print "<option value=\"Network\" @graphselected[2]>Show network traffic type Graphs</option>";
	print "<option value=\"Farm\" @graphselected[3]>Show farm type Graphs</option>";
	print "</select>";
	print "<input type=\"hidden\" name=\"id\" value=\"$id\" />";
	print "<br />";
	print "<br />";
	print "<input type=\"submit\" value=\"Select Graph type\" name=\"action\" class=\"button small\" />";
	print "</form>";
	print "<br />";

	if ( $graphtype =~ /^$/ || $graphtype eq "All" )
	{
		@gtypes = ( System, Network, Farm );
		foreach $gtype ( @gtypes )
		{
			@graphlist = &getGraphs2Show( $gtype );
			foreach $graph ( @graphlist )
			{
				print "<div class=\"tc\"><a href=\"?id=$id&amp;action=$graph\"><img src=\"img/icons/small/zoom_in.png\" title=\"More info\" alt=\"[z]\" /></a>";
				print '<img src="data:image/png;base64,' . &printGraph( $graph, "d" ) . '" alt="[Graph]" />';
				print "</div><br /><br />";
			}
		}
	}
	else
	{
		@graphlist = &getGraphs2Show( $graphtype );
		foreach $graph ( @graphlist )
		{
			print "<div class=\"tc\"><a href=\"?id=$id&amp;action=$graph\"><img src=\"img/icons/small/zoom_in.png\" title=\"More info\" alt=\"[z]\" /></a>";

			#print "<img src=\"img/graphs/$graph\" alt=\"[Graph]\" /></div><br /><br />";
			print '<img src="data:image/png;base64,' . &printGraph( $graph, "d" ) . '" alt="[Graph]" />';
			print "</div><br /><br />";
		}
	}
	print "</div></div></div>";
}

}

print "<br class=\"cl\" />";

print "        </div>
    <!--Content END-->
";
