# Yet another Graph API Implementation

Why? Oh why? Why did I not call this YAGAI? Anyway, why do we need another implementation?

We probably don't. But the existing implementations I could find did not have the features I needed,
and/or were not easy enough to extend. 

Here are a few very basic components that will help you compose the features you need (hopefully). 

Lots of features missing though. YMMV. 

## Core API

At the core of the API is the `GraphClient` that is used for making a request. There are
two default implementations included:

* [RequestsGraphClient](./msgraphy/client/graph_client.py)
* [BatchGraphClient](./msgraphy/client/graph_batch.py)

and both use the [Requests](https://requests.readthedocs.io/en/master/) library for making the 
request.

## Authentication

Authentication is provided by passing any callable in the constructor of the `GraphClient`.
The callable takes no arguments and is expected to return the current bearer token.

Some components are [provided](./msgraphy/auth/graph_auth.py) to help with authentication:

* BasicAuth - Configuration based on environment variables, or a provided 'config' object.
* ConfidentialTokenWrapper - If you need more specific control over the token, you can use this 
  wrapper to obtain a token from a client_id and client_secret.
* InteractiveTokenWrapper - If you need more specific control over the token, you can use this 
  wrapper to obtain a token using device flow authentication.

These can very simply be composed to provide the authentication you need, and all use the 
[Microsoft Authentication Library (MSAL) for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/active-directory?view=azure-python).

