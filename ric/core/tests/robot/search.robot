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
    Wait until page contains element  css=div#ric-search-warning
    Wait until page contains  Vous devez compléter votre description (Haddock) pour pouvoir effectuer une recherche.


Test search with organization member organization uncompleted profile
    Log in  dupont  secret
    Go to  ${PLONE_URL}/annuaire
    Input text  name=form.widgets.contentName  imio
    Click button  Rechercher
    Wait until page contains element  css=div#ric-search-warning
    Wait until page contains  Vous devez compléter la description de votre organisation (Imio) pour pouvoir effectuer une recherche.


Test search with anonymous
    Go to  ${PLONE_URL}/annuaire
    Wait until page contains element  css=div#ric-search-error
