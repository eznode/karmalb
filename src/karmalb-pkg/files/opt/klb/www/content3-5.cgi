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

use File::stat;
use File::Basename;
use Time::localtime;
use Sys::Hostname;
my $host = hostname();

print "
<!--Content INI-->
<div id=\"page-content\">

<!--Content Header INI-->
<h2>Settings::Backup</h2>
<!--Content Header END-->";

if ( $action eq "diff" )
{
	print "<div class=\"box-header\">";
	print "Configuration Differences with $file";
	print "</div>";
	print "<div class=\"box stats\">";
	print "<div style=\"white-space: pre ; display: block; unicode-bidi: embed; font-family: monospace; font-size: 120%; border: 1px solid black\">";
	my $output = `$zenbackupdiffscript $backupdir$file $backupfor`;
        print CGI::escapeHTML( $output );
	print "</div>";
	print "</div>";
}

if ( $action eq "apply" )
{
	&successmsg( "Backup will be decompressed and Karma Load Balancer will be restarted, ZLB Cluster node could switch..." );
	my @eject = `$zenbackupextscript $backupdir$file $backupfor`;
	&logfile( "Restoring backup $backupdir$file" );
	&logfile( "unpacking files: @eject" );
	my @eject = `/etc/init.d/zenloadbalancer restart 2> /dev/null`;
	if ( $? == 0 )
	{
		&successmsg( "Backup applied and Karma Load Balancer restarted..." );
	}
	else
	{
		&errormsg( "Problem restarting Karma Load Balancer service" );
	}

}

if ( $action eq "Create Backup" )
{
	if ( $name !~ /^$/ && $name =~ /^[a-zA-Z0-9\-]*$/ )
	{
		$name =~ s/\ //g;
		my @eject = `$zenbackup $name -c 2> /dev/null`;
		&successmsg( "Local system backup created <b>backup-$name.tar.gz</b>" );
	}
	else
	{
		&errormsg( "Backup name is not valid. Only numbers, letters and hyphens are allowed." );
	}
}

if ( $action eq "del" )
{
	$filepath = "$backupdir$file";
	if ( -e $filepath )
	{
		unlink ( $filepath );
		&successmsg( "Deleted backup file <b>$file</b>" );

	}
	else
	{
		&errormsg( "File <b>$file</b> not found" );
	}

}

#if ($action eq "Upload Backup")
#	{
#$CGI::POST_MAX = 1024 * 5000;
#my $query = new CGI;
#my $safe_filename_characters = "a-zA-Z0-9_.-";
#my $upload_dir = "$backupdir";
#my $filex = $query->param("file");
#my $upload_filehandle = $query->upload("fileName");
#
#open ( UPLOADFILE, ">$backupdir$file" ) or die "$!";
#binmode UPLOADFILE;
#
#while ( <$upload_filehandle> )
#{
# print UPLOADFILE;
#}
#
#close UPLOADFILE;
#	}

print "<div class=\"container_12\">";
print "	<div class=\"grid_12\">";
print "		<div class=\"box-header\">Backup</div>";
print "		<div class=\"box stats\">";

print "<form method=\"get\" action=\"index.cgi\">";
print "<b>Description name: </b><input type=\"text\" name=\"name\" value=\"$lhost\" />";
print "<input type=\"hidden\" name=\"id\" value=\"$id\" />";
print "<input type=\"submit\" value=\"Create Backup\" name=\"action\" class=\"button small\" />";
print "</form>";
print "<br /><br />";

print "</div></div></div>";
print "<br class=\"cl\" />";

#table
print "<div class=\"box-header\"> Backup files <a href=\"index.cgi?id=$id\"><img src=\"img/icons/small/arrow_refresh.png\" title=\"refresh\" alt=\"[Refresh]\" /></a></div>";
print "<div class=\"box table\">";

print "<table>";
print "<thead>";

print "<tr>";
print "<th>Description name</th>";
print "<th>Date</th>";
print "<th>Host</th>";
print "<th>Action</th>";
print "</tr>";
print "</thead>";
print "<tbody>";

opendir ( DIR, "$backupdir" );
@files = grep ( /^backup.*/, readdir ( DIR ) );
closedir ( DIR );

foreach $file ( @files )
{
	print "<tr>";
	$filepath = "$backupdir$file";
	chomp ( $filepath );

	#print "filepath: $filepath";
	$datetime_string = ctime( stat ( $filepath )->mtime );
	print "<td>$file</td>";
	print "<td>$datetime_string</td>";
	print "<td>$host</td>";
	print "<td>";
	&createmenubackup( $file );
	print "</td>";
	print "</tr>";
}

print "<tr><td colspan=\"3\"></td><td>";

&upload();

print "</td></tr>";
print "</tbody>";
print "</table>";
print "</div>";

#print "		</div>";
#print "<br />";
#print "	</div>";
#print "</div>";

print "<br class=\"cl\" />";

#content 3-4 END
print " </div>
    <!--Content END-->
";

