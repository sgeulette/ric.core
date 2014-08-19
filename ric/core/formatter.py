from datetime import datetime
from z3c.form.converter import IntegerDataConverter


class RICIntegerDataConverter(IntegerDataConverter):
    """A data converter for integers that doesn't convert years."""

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        if value >= 1900 and value <= datetime.now().year:
            return str(value)
        return self.formatter.format(value)
