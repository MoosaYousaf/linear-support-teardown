# Addition: fetching an issue by its identifier (ENG-123)

**Pages:** https://linear.app/developers/sdk-fetching-and-modifying-data and https://linear.app/developers/graphql

**Why.** Two developers asked the same question eight months apart (#765, July 2025; #1066, March 2026).
#1066 was closed under an internal ticket titled "GraphQL docs: clarify that IssueFilter does not support
issue [identifier]", but none of the developer guide pages mention it (checked 2026-10-28; the fix may
live in the GraphQL schema reference, which this audit did not crawl). The schema describes `issue(id:)`
only as "looked up by its unique identifier", and "identifier" means the UUID in some places and
`ENG-123` in others.

**Proposed text:**

> ### Fetch an issue by its identifier
> `issue` accepts either the issue's UUID or its human-readable identifier:
> ```ts
> const issue = await linearClient.issue("ENG-123");
> ```
> ```graphql
> query { issue(id: "ENG-123") { id identifier title } }
> ```
> To fetch several issues from one team at once, filter on the team key and issue numbers.
> `IssueFilter` has no `identifier` field:
> ```graphql
> query {
>   issues(filter: { team: { key: { eq: "ENG" } }, number: { in: [123, 124, 130] } }) {
>     nodes { id identifier title }
>   }
> }
> ```

*Basis: `IssueFilter.team`, `TeamFilter.key` and `NumberComparator.in` exist in the published schema
(`packages/sdk/src/schema.graphql`), and the reporter of #1066 confirmed direct lookup by identifier works.
Not run against the live API; test before publishing.*
