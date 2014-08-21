*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test user menu action
    Log in as site owner
    Go to  ${PLONE_URL}
    Open user menu
    Click link  css=li#personaltools-ric_send_mail a
    Wait until page contains  Envoi d'e-mails


Test edit mail template
    Log in as site owner
    Go to  ${PLONE_URL}/send_mail
    Click link  css=a#edit_non_contributor
    Page should contain  Modifier l'action d'envoi de courriel
    Input text  name=form.message  Nouvelle template
    Click Button  Enregistrer
    Page should not contain  Modifier l'action d'envoi de courriel
    Click link  css=a#edit_non_contributor
    Page should contain  Nouvelle template
