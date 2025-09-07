# Sub-Modules
- api/
- - HTTP/interface from db to anything else
- - bulk of logic of server/ module
- db/
- - storage layer
- - houses db/Seed/ sub-module for seeding test data
- auth/
- - handle authorization/cryptography
- - should this go under api/ sub-module?
- util/
- - miscellaneous python tools that can be used in any other sub-module

# Architexture of api/ sub-module
gateway.py is the main file

Sub-modules under api/ are nested (maybe not ideal?)
- orchestrator/
- - the main brain of the module (very nested as of now)
- Routers/
- - catalogue of HTTP routes
- tests/
- - automated tests
- util/
- - tools different from server/util/ that are specific to api/ things

# Architexture of api/orchestrator/ sub-module
orchestrator.py is main file that handles logic of various features of the api

Sub-modules under orchestrator/
- Cache
- - handle Redis-like caching of DB data to optimize latency
- - currently no work done on this as not top priority 
- session
- - where the logic drills down into servicing different sessions for different users
- - many features (or basic functions of modern web-apps?) are handled here
- - - anonymous sessions and user sessions
- - - login/logout/register
- storage
- - handling of cloud storage vs local testing of storage
- - videos and images

# Concerns of this architexture
This feels like a monumental amount of code for basic features of a web-app. As of now, the web-site cannot do much.
Are there basic boilerplate libraries or flask tools that I could have used to make these files simpler?
Perhaps even basic behaviour of modern web-apps like Youtube are more complex than they seem. Making things seamless
is not seamless to do.