from spark import Spark
from spark import SparkRoom

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
print("title is: " + room.title)
print("created at: " + room.created)
print("last activity at: " + room.lastActivity)
print("room type is: " + ("group" if (room.type == SparkRoom.GROUP) else "1:1")
      + " chat")
