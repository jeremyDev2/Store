import graphene
import products.ql_schema

class Query(products.ql_schema.Query, graphene.ObjectType): ...

schema = graphene.Schema(query=Query)
