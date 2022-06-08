import graphene
from saleor.graphql.core.utils import from_global_id_or_error
from saleor.graphql.core.fields import FilterInputConnectionField, \
    PrefetchingConnectionField

from .mutations import TransferRequestCreate
from .types import TransferRequest
from .resolvers import resolve_transfer_requests, resolve_transfer_request


class TransferRequestQueries(graphene.ObjectType):
    transfer_request = graphene.Field(
        TransferRequest,
        description="Look up a transfer request by ID.",
        id=graphene.Argument(
            graphene.ID, description="ID of an transfer request.", required=True
        ),
    )

    transfer_requests = PrefetchingConnectionField(TransferRequest,
                                                   description="List of transfer request.")

    def resolve_transfer_request(self, info, **kwargs):
        transfer_request_pk = kwargs.get("id")
        _, id = from_global_id_or_error(transfer_request_pk, TransferRequest)
        return resolve_transfer_request(id)

    def resolve_transfer_requests(self, info, **_kwargs):
        return resolve_transfer_requests()


class TransferRequestMutations(graphene.ObjectType):
    transfer_request_create = TransferRequestCreate.Field()
    # update_custom = CustomUpdate.Field()
    # delete_custom = CustomDelete.Field()
    # custom_clone = CustomClone.Field()
