from spark import Spark

bearerToken = "an example"
rooms = Spark.using(bearerToken).rooms().get()

print("Room titles are:")
for room in rooms:
    print(room.title)
