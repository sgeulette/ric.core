*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test profile completed viewlet
    Log in  tintin  secret
    Go to  ${PLONE_URL}
    Wait until page contains  Tin Tin
    Page should not contain  Votre description comprend plus de 15% de données non remplies.


Test profile not completed viewlet
    Log in  haddock  secret
    Go to  ${PLONE_URL}
    Wait until page contains  haddock
    Wait until page contains  Votre description comprend plus de 15% de données non remplies.


Test organization completed viewlet
    Log in  tintin  secret
    Go to  ${PLONE_URL}
    Wait until page contains  Tin Tin
    Pause
    Page should not contain  La description de votre organisation comprend plus de 15% de données non remplies. 

Test organization not completed viewlet
    Log in  dupont  secret
    Go to  ${PLONE_URL}
    Wait until page contains  dupont
    Wait until page contains  La description de votre organisation comprend plus de 15% de données non remplies. 
