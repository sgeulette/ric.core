*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test example
    Log in as site owner
    Go to  ${PLONE_URL}/createObject?type_name=directory
    Input text  name=form.widgets.IBasic.title  Annuaire
    Input text  name=form.widgets.position_types.AA.widgets.name  President
    Input text  name=form.widgets.organization_types.AA.widgets.name  ASBL
    Input text  name=form.widgets.organization_levels.AA.widgets.name  Niveau
    Click Button  Save
    Click Action by id  rename
    Input text  name=new_ids:list  annuaire
    Click Button  Rename All
    Go to  ${PLONE_URL}/annuaire/createObject?type_name=organization
    Input text  name=form.widgets.IBasic.title  Organization
    Input text  name=form.widgets.habitants  100
    Input text  name=form.widgets.serveurs  Linux
    Input text  name=form.widgets.logiciels  Firefox
    Click Button  Save
