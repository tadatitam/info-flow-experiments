# Testing Harness

## Overview

The most efficient method to test this ad collection module is directly from the python repl. 

`python`

These are some helpful testing harness commands. Copy and paste the utility functions directly into the repl, then run them as indicated below to test.

## Commands

### Import code and update on changes to source

To import unit

`import adbtest_unit`

To reload after you have made changes to the source

`reload(adbtest_unit)`

Create a new browser session after reloading

`a = adbtest_unit.AdbTestUnit()`

This can be combined into the utility function

```
def update():
    reload(adbtest_unit)
    return adbtest_unit.AdbTestUnit()
```

Called like this:

a = update()

### Test visiting sites and checking ads there

Visit a site like:

`a.visit_url(site)`

Test collecting  ads using these functions:

`a.find_href_ads()`
`a.find_src_ads()`
`a.check_iframes()`

Or all inclusive with:

`a.find_ads()`


This can be combined into the utility function

```
def go():
    a.visit_url(site)
    print "start ad collection"
    a.find_ads()
```

Called like this:

`go()`


### Common sites to test

site = "http://www.foxnews.com/us/index.html"
site = "http://www.reuters.com/news/us"
site = "http://www.bbc.com/news"


## Common use case

site = "http://www.bbc.com/news"
a = update()
go()

