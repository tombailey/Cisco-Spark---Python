from spark import Spark

bearerToken = "an example"
room = Spark.using(bearerToken).rooms().get()[0]
# Spark on supports single URLs at the moment
files = ("https://www.ciscospark.com/etc/designs/ciscospark/eopi/images/"
         "squared-logo-130.png")

sent = Spark.using(bearerToken).room(room).message(files=files).post()
print("Message" + (" not" if not sent else "") + " posted to room")
