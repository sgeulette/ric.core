jQuery(document).ready(function($) {

    $('div.edit_mail_template a').prepOverlay({
        subtype: 'ajax',
        filter: '#content>*',

        formselector:'form',
        noform: 'reload', 
        beforepost: function(form, form_data) {
            $('div.close').click();
            return true;
        }

    });

});
