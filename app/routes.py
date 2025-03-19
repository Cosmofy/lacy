import strawberry
from strawberry.fastapi import GraphQLRouter
from app.resolvers import Query

# Create GraphQL Schema
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)