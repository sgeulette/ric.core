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
    Wait Until Page Contains Element  css=a#edit_non_contributor  10
    Click link  css=a#edit_non_contributor
    Page should contain  Edit Mail Action
    Input text  name=form.message  Nouvelle template
    Click Button  Save
    Go to  ${PLONE_URL}/send_mail
    Wait Until Page Contains Element  css=a#edit_non_contributor  10
    Click link  css=a#edit_non_contributor
    Page should contain  Nouvelle template


Test send mail
    Log in as site owner
    Go to  ${PLONE_URL}/send_mail
    Wait Until Page Contains Element  css=input#submit_non_contributor  10
    Click button  css=input#submit_non_contributor
    Wait until page contains  E-mail envoyé à:
