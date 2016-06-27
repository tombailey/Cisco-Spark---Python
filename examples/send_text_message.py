from spark import Spark

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
message = "Hello world!"

sent = Spark.using(bearerToken).room(room).message(message).post()
print("Message" + (" not" if not sent else "") + " posted to room")
