from zope.annotation.interfaces import IAnnotations

KEY = "ric.core.old_email"


def edit_begun(event):
    """
    When editing person, we store the email address
    """
    obj = event.object
    if obj.portal_type != 'person':
        return
    annotations = IAnnotations(obj)
    annotations[KEY] = obj.email


def edit_canceled(event):
    """
    If the edit is cancelled, we can delete the stored email address value
    """
    obj = event.object
    if obj.portal_type != 'person':
        return
    annotations = IAnnotations(obj)
    del annotations[KEY]


def edit_modified(event):
    """
    When editing is finished, we can compare old and new email address values
    and uncheck 'invalid mail' field if the address was changed
    """
    obj = event.object
    if obj.portal_type != 'person':
        return
    annotations = IAnnotations(obj)
    oldEmail = annotations[KEY]
    if oldEmail != obj.email:
        obj.invalidmail = False
