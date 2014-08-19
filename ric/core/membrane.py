from collective.contact.membrane.behaviors.personmembraneuser import PersonMembraneUserAdapter


class RICPersonMembraneUserAdapter(PersonMembraneUserAdapter):

    def getUserName(self):
        if self.context.userid:
            return self.context.userid
        else:
            return super(RICPersonMembraneUserAdapter, self).getUserName()
