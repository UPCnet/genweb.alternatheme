import sys

# default is to run locally
use_ondemand = "false"

# add the left/right decision
for arg in sys.argv:
    if arg.startswith("--ondemand"):
        parts = arg.split("=")
        use_ondemand = parts[1].lower()

if use_ondemand == "true":
    ZSERVER_PORT = "4001"
    REMOTE_URL = 'http://sneridagh:4ad2774f-dd79-446d-81de-624308149a16@ondemand.saucelabs.com:80/wd/hub'
    DESIRED_CAPABILITIES = 'browserName:internet explorer,javascriptEnabled:True,platform:Windows 2012,version:10,name:Testing Genweb in Firefox 17 on MAC'
    SELENIUM_HOST = "ondemand.saucelabs.com"
    SAUCE_USERNAME = "your-sauce-user"
    SAUCE_KEY = "your-sauce-key-here"
    SAUCE_OS = "Windows 2003"
    SAUCE_BROWSER = "firefox"
    SAUCE_VERSION = "3."
    SAUCE_NAME = "Robots everywhere!"
    BROWSER = '{"username": "%s", "access-key": "%s", "os": "%s", "browser": "%s", "browser-version": "%s", "name": "%s"}' % (SAUCE_USERNAME, SAUCE_KEY, SAUCE_OS, SAUCE_BROWSER, SAUCE_VERSION, SAUCE_NAME)
else:
    ZSERVER_PORT = 55001
