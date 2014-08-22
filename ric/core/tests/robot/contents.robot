*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test example
    Log in as site owner
    Go to  ${PLONE_URL}/folder_factories
    Wait Until Page Contains Element  css=input#form-field-directory  10
    Select Radio Button  url  form-field-directory
    Click Button  Add
    Input text  name=form.widgets.IBasic.title  Annuaire
    Input text  name=form.widgets.position_types.AA.widgets.name  President
    Input text  name=form.widgets.organization_types.AA.widgets.name  ASBL
    Input text  name=form.widgets.organization_levels.AA.widgets.name  Niveau
    Click Button  Save
    Go to  ${PLONE_URL}/annuaire-1/folder_factories
    Wait Until Page Contains Element  css=input#form-field-organization  10
    Select Radio Button  url  form-field-organization
    Click Button  Add
    Input text  name=form.widgets.IBasic.title  Organisation
    Input text  name=form.widgets.IRICOrganization.citizen  100
    Input text  name=form.widgets.IRICOrganization.servers  Linux
    Input text  name=form.widgets.IRICOrganization.softwares  Firefox
    Click element  css=#fieldsetlegend-contact_details
    Input text  name=form.widgets.IContactDetails.email  example@organisation.com
    Click Button  Save
    Page should contain  Item created
