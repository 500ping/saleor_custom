import graphene
from saleor.graphql.core.mutations import ModelMutation
from saleor.warehouse.models import Stock
from saleor.graphql.warehouse.types import Warehouse
from saleor.core.permissions import AccountPermissions
from .TransferRequestError import TransferRequestError, TransferRequestErrorCode
from .types import TransferRequest as TransferRequestType
from .. import models


def check_stock_quantity(source, quantity_requested, product_variant):
    warehouse = Stock.objects.filter(warehouse=source,
                                     product_variant=product_variant).first()
    if not warehouse:
        raise TransferRequestError(
            code=TransferRequestErrorCode.PRODUCT_NOT_IN_WAREHOUSE)
    if warehouse.annotate_available_quantity() < quantity_requested:
        raise TransferRequestError(code=TransferRequestErrorCode.STOCK_NOT_VALID)


class TransferRequestCreateInput(graphene.InputObjectType):
    source_warehouse = graphene.ID(description='Source warehouse global id.',
                                   required=True)
    dest_warehouse = graphene.ID(description='Source destination global id.',
                                 required=True)
    quantity = graphene.Int(description='Product quantity', required=True)
    product_id = graphene.ID(description='Product global id.', required=True)


class TransferRequestCreate(ModelMutation):
    class Arguments:
        input = TransferRequestCreateInput(
            required=True, description="Fields required to create a transfer request."
        )

    class Meta:
        description = "Creates a new transfer request."
        model = models.TransferRequest
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = TransferRequestError
        error_type_field = "transfer_request_errors"

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        user = info.context.user
        if user.is_authenticated:
            instance.created_by = user
        return instance

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)

        quantity = cleaned_input.get("quantity")
        source_id = cleaned_input.get("source_warehouse")
        product_id = cleaned_input.get("product_id")

        check_stock_quantity(source_id, quantity, product_id)

        return cleaned_input
