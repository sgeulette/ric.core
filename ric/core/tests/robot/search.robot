*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test search with admin
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire
    Input text  name=form.widgets.contentName  affinitic
    Click button  Rechercher
    Wait until page contains element  css=div#ric-search-results li.result a


Test search with organization member completed profile
    Log in  tintin  secret
    Go to  ${PLONE_URL}/annuaire
    Input text  name=form.widgets.contentName  affinitic
    Click button  Rechercher
    Wait until page contains element  css=div#ric-search-results li.result a


Test search with organization member uncompleted profile
    Log in  haddock  secret
    Go to  ${PLONE_URL}/annuaire
    Input text  name=form.widgets.contentName  affinitic
    Click button  Rechercher
    Wait until page contains  Vous ne pouvez pas effectuer de recherche


Test search with anonymous
    Go to  ${PLONE_URL}/annuaire
    Wait until page contains  Il faut être membre du RIC et connecté au site pour pouvoir effectuer des recherches dans l'annuaire. 
