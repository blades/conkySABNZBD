conkySABNZBD

Intially created 24/09/2010 by blades <blades@gecko.org.uk>
Updated 13/03/2018 by blades <blades@gecko.org.uk>

Improved version of the sabnzbdcli code created by Sabooky 
(https://forums.sabnzbd.org/viewtopic.php?f=6&t=391&p=1752&hilit=sabapi#p1752)
Uses code from Kaivalagi's conkyForecast 
(http://www.kaivalagi.com/blog/) for reading in a template 
file and filling in the template, although it's been altered to suit the 
requirements of this project.

This was put together in about a day to improve the sabnzbd cli 
interface and associated conky code created by Sabooky.  The 
improvements were required as SABNZBD has a new information interface 
via the api provided by the server.  The output from the Sabooky 
code was also limited to certain pieces of information, and the 
configuration was performed by hacking the code manually.

I also wanted to add templating for the output, and to be able to make 
use of any of the returned information from the SABNZBD api query.

As such, the code was substantially rewritten (although the API code 
created by Sabooky remains more or less intact - only the call to the 
query api was changed to return the output from the api call, and to 
handle errors elsewhere in the code).

Usage: conkySABNZBD.py [options]

Options:
  -h, --help            show this help message and exit
  -c CONFIGFILE, --config=CONFIGFILE
                        Path to sabnzbd.ini file (or a config file
                        containing name=value pairs for api_key, 
                        host and port under a [misc] section).
                        Will default to /opt/sabnzbd/sabnzbd.ini
                        if not otherwise specified.
  -t TEMPLATEFILE, --template=TEMPLATEFILE
                        Path to template output file
  -j JOBTEMPLATEFILE, --jobtemplate=JOBTEMPLATEFILE
                        Path to job template output file
  -k JOBCOUNT, --jobcount=JOBCOUNT
                        Number of jobs to write out

In terms of what can be done in the templates, the output from the api call 
(http://[sabhost]:[sabport]/sabnzbd/apit?output=json&apikey=[yourapikey]&mode=queue) 
provides the content for the templates.  The template output file can 
use the name of any of the elements under query that have a value (e.g. 
[noofslots] will be replaced with the value of the noofslots element).  
The job template file similarly will write out the value of the elements 
under the query/slots/slot element (e.g. [filename] will write out the 
value of the filename element).  Note that I'm talking about elements 
here, but the api call returns the json representation, not the xml 
representation.

The job count value controls the number of slots that will be written 
out in the template.  To display this output, add a [jobs] tag into the 
main template, and the call will replace that tag with a loop over the 
number of jobs specified to write out the job template for each job.  
The default is to write out all slots in the output.

I don't intend to do any more development on this at present as it 
currently does everything that I need it to (and a bit more as I 
suffered from feature creep while I was coding it), but should you have 
any more features that you'd like to see, or you find some bugs (or just 
want to tidy up any code that's not as good as it could be) then drop me 
an email at blades@gecko.org.uk with conkySABNZBD in the subject line and 
I'll get back to you when I can.
