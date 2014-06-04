*** Settings ***

Variables  plone/app/testing/interfaces.py
Variables  genweb/alternatheme/tests/robot/variables.py
#Variables  saucelabs.py

Library  Selenium2Library  timeout=${SELENIUM_TIMEOUT}  implicit_wait=${SELENIUM_IMPLICIT_WAIT}

# Resource  library-settings.txt
Resource  genweb/alternatheme/tests/robot/keywords.txt

Suite Setup  Suite Setup
Suite Teardown  Suite Teardown

*** Test Cases ***

Genweb Basic Setup
    Log in as manager
    Page should contain  You are now logged in

*** Keywords ***

Goto homepage
    Go to  ${PLONE_URL}
    Page should contain  Plone site

Log in as manager
    Go to  ${PLONE_URL}/login_form
    Click Element  link=Log in only in this site
    Page should contain element  __ac_name
    Input text  __ac_name  ${TEST_USER_NAME}
    Input text  __ac_password  ${TEST_USER_PASSWORD}
    Click Button  Log in
    Page should contain element  css=.user
