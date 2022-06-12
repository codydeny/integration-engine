# Design - Pros and Cons
## Approach 1 basic:
Using a simple `handler` to `enum` mapper dict/map that would keep track of which `handler` to call for which `enum` value.
### Example
```
# in python
handler_to_enum_map = {
    "GOOGLE_DOCS" : "GoogleDocsHandler",
    "ZAPIER" : "ZapierHandler"
}
```
then define `handler`
```
def GoogleDocsHandler(data):
    # do something soemthing
    return new_data
```
### Approach 2 (Current):
so current approach is an evolution of the basic one, but rather than using `handler` functions, it uses `Integration` classes. Classes here have encapsulated a lot of repeating behaviour and helped in DRY code.

# Integration Processor/Engine
This module/part actually executes the integrations and is responsible for their management, updating status, keeping track of each step's data,etc.

It again encapsulates a lot of funcitonality that could have been repeated, if we just had a `handler`.

# trigger
Currenlty integrations work in 2 step, first is `initialization` and second is `execution`. So `initialization` takes place when a user creates an integration on a form while `execution` takes place on every response submission. One response submission contains `n` number of answers all at once. They either get 'accepted' or 'rejected' based on the output of the `integration execution`