# Cisco-Spark---Python

## Introduction

This is a Python based library to communicate with [Cisco's Spark API](https://developer.ciscospark.com/getting-started.html); v1 to be precise.

It allows you to:

1. Retrieve a list of rooms
2. Retrieve information about a room (title, created time, etc)*
3. Create new rooms
4. Retrieve a list of messages for a room*
5. Creating new messages in a room*

*requires you to have a bearer token for a user that is already in the target room.

No attempt is made to handle OAuth, that is something you need to handle as per [the documentation](https://developer.ciscospark.com/authentication.html).

## Dependencies

1. [requests](http://docs.python-requests.org/en/master/)
2. [json](http://docs.python-guide.org/en/latest/scenarios/json/)

## Examples

Provided in ./examples but also as below:

Create a room named "Example"
```python
from spark import Spark

bearerToken = "an example"
newRoom = Spark.using(bearerToken).room().create("Example")
print("Room" + (" not" if not newRoom else "") + " created")
```

List the rooms a user is in
```python
from spark import Spark

bearerToken = "an example"
rooms = Spark.using(bearerToken).rooms().get()

print("Room titles are:")
for room in rooms:
    print(room.title)

```

Retrieve information about a particular room
```python
from spark import Spark
from spark import SparkRoom

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
print("title is: " + room.title)
print("created at: " + room.created)
print("last activity at: " + room.lastActivity)
print("room type is: " + ("group" if (room.type == SparkRoom.GROUP) else "1:1")
      + " chat")
```

Send a textual message to a room
```python
from spark import Spark

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
message = "Hello world!"

sent = Spark.using(bearerToken).room(room).message(message).post()
print("Message" + (" not" if not sent else "") + " posted to room")
```

Send an image message to a room (works for any file but [Spark only renders a preview for a few](https://developer.ciscospark.com/attachments.html))
```python
from spark import Spark

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
# Spark on supports single URLs at the moment
files = ("https://www.ciscospark.com/etc/designs/ciscospark/eopi/images/"
         "squared-logo-130.png")

sent = Spark.using(bearerToken).room(room).message(files=files).post()
print("Message" + (" not" if not sent else "") + " posted to room")
```



##



## License

Apache 2 (go mad)
