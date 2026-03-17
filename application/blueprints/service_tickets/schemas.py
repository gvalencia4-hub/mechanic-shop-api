from ...extensions import ma
from ...models import ServiceTicket, Mechanic


class MechanicNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "specialty")


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Nested(MechanicNestedSchema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)