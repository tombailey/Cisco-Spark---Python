from spark import Spark

bearerToken = "an example"
newRoom = Spark.using(bearerToken).room().create("Example")
print("Room" + (" not" if not newRoom else "") + " created")
