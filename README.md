vera-eventghost
===============

Vera plugin for EventGhost

Installation
------------

To install simple copy the folder "Vera" into your eventghost plugin folder, then activate
 the plugin in EventGhost
 
Using in non-Eventghost programs
--------------------------------

The VeraClient class used by this plugin can easily be incorporated into other Python 
programs. When used in EventGhost it uses the Asyncore event loop, but it can just as 
easily be used with Twisted. The root directory has a replacement dispatcher to be used
with Twisted to fetch web pages, and a simple test script that can be run outside of 
EventGhost for both the Asyncore and Twisted event loops.