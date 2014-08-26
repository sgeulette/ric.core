*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test userid invariant valid
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/haddock/edit
    Click Button  Save
    Page should not contain  Utilisateur déjà existant

Test userid invariant invalid
    Log in as site owner
    Go to  ${PLONE_URL}/annuaire/affinitic/haddock/edit
    Input text  name=form.widgets.IRICPerson.userid  tintin
    Click Button  Save
    Wait Until Page Contains  Utilisateur déjà existant
