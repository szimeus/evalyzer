# evalyzer
Use WinDBG to tap into JavaScript and help with deobfuscation and browser exploit detection!

Steps to start creating your own JavaScript malware analyzer in IE11
We’re going to set up an environment that allows a malware analyst to log all JavaScript eval operations without giving a chance to the malicious page to ever realize it is being debugged. Unlike the popular methods that rely either on workarounds that run the script in an external JS engine or injecting script code to overload eval function or add event handling or single stepping and breakpointing in the built-in browser script debuggers, we’re going to tap into the real JS Engine to log everything that is being eval’d. To do this we’re going to use WinDBG – in fact the command-line version of it, called NTSD.exe. The below write-up summarizes the steps needed to make this work in IE11. However the same method could be re-tailored to work in every other browser, so if you pay attention and follow along and understand why this works and how it works I’m sure it would only take you a short while to customize it to your environment.

Prerequisites:

Make sure you use the same bitness (x86 or x64) across all components (python, pykd, windbg)!

1.	python 2.7
2.	WinDBG
  -	set up symbols 
    o	if you’re new to this just add the below to system environment vars:
      _NT_SYMBOL_PATH = SRV*c:\symbols*http://msdl.microsoft.com/download/symbols
    (If you’re going to work with Chrome you’ll need different symbols!!
      _NT_SYMBOL_PATH= SRV*c:\symbols\chrome*https://chromium-browser-symsrv.commondatastorage.googleapis.com)
3.  Corelan's mona for WinDBG https://github.com/corelan/windbglib/blob/master/README.md 
    (TL;DR: put the following into windbg's x86|x64 folder: windbglib.py, mona.py, winext/pykd.pyd and register msdia90.dll or msdia120.dll)
4.  chain.py (contained in this repo) - copy file to windbg x86|x64 folder


Read the Evalyzer_tutorial.pdf to understand the technique!

How to use it:

1.  Fire up an IE11 browser

2.  run IELog.ps1

3.  navigate to the URL containing the javascript to be analyzed

4.  check the logs
__________
[Added materials from BSides Budapest 2017 workshop](http://htmlpreview.github.io/?https://raw.githubusercontent.com/szimeus/evalyzer/master/BSides%20Budapest%202017%20workhop%20materials.html)



