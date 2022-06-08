import graphene
from .. import models
from saleor.warehouse.models import Warehouse
from saleor.graphql.core.connection import CountableDjangoObjectType


class TransferRequest(CountableDjangoObjectType):
    id = graphene.GlobalID(required=True)

    # source_warehouse = graphene.Field(Warehouse, description="Return source warehouse.")
    # dest_warehouse = graphene.Field(Warehouse, description="Return source destination "
    #                                                        "warehouse.")

    class Meta:
        model = models.TransferRequest
