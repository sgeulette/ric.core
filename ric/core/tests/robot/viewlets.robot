*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test 'invalid mail' viewlet
    Log in  tintin  secret
    Go to  ${PLONE_URL}
    Wait until page contains  Tin Tin
    Element should be visible  css=#ric-email-viewlet
    Click link  css=#ric-email-viewlet a
    Input text  name=form.widgets.IContactDetails.email  supertintin@affinitic.be
    Click Button  Save
    Element should not be visible  css=#ric-email-viewlet


Test 'contact cotisation' viewlet
    Log in  dupont  secret
    Go to  ${PLONE_URL}
    Wait until page contains  Dupont
    Element should be visible  css=#ric-cotisation-viewlet
    Go to  ${PLONE_URL}/annuaire/imio/dupont/edit
    Click element  css=#form-widgets-IRICPerson-multimail-from option
    Click element  name=from2toButton
    Click Button  Save
    Go to  ${PLONE_URL}
    Element should not be visible  css=#ric-cotisation-viewlet


Test 'profile completion' viewlet for person
    Log in  dupont  secret
    Go to  ${PLONE_URL}
    Wait until page contains  Dupont
    Element should be visible  css=#ric-profile-viewlet .person-link
    Click link  css=#ric-profile-viewlet a.person-link
    Go to  ${PLONE_URL}/annuaire/imio/dupont/edit
    Input text  name=form.widgets.firstname  Jean
    Click element  css=#fieldsetlegend-contact_details
    Input text  name=form.widgets.IContactDetails.phone  1234
    Input text  name=form.widgets.IContactDetails.cell_phone  1234
    Input text  name=form.widgets.IContactDetails.fax  1234
    Input text  name=form.widgets.IContactDetails.website  http://www.google.com
    Click element  css=#fieldsetlegend-address
    Input text  name=form.widgets.IContactDetails.number  1
    Input text  name=form.widgets.IContactDetails.street  Rue haute
    Input text  name=form.widgets.IContactDetails.zip_code  1500
    Input text  name=form.widgets.IContactDetails.city  SuperCity
    Input text  name=form.widgets.IContactDetails.region  Here
    Click Button  Save
    Element should not be visible  css=#ric-profile-viewlet .person-link
