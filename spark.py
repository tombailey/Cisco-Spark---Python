# TODO: support people, memberships and webhooks resources
import requests
import json


class SparkRoom:
    # for 1:1 rooms (as per
    # https://developer.ciscospark.com/endpoint-rooms-get.html)
    DIRECT = "direct"
    # for group rooms (as per
    # https://developer.ciscospark.com/endpoint-rooms-get.html)
    GROUP = "group"

    id = None
    title = None
    type = None
    locked = None
    lastActivity = None
    created = None

    def __init__(self):
        pass

    def fromDictionary(dict):
        '''Creates a SparkRoom according to the dictionary given. Typically,
        this dictionary comes from a JSON object given by the Spark API'''
        room = SparkRoom()
        room.id = dict["id"]
        room.title = dict["title"]
        room.type = dict["type"]
        room.locked = dict["isLocked"]
        room.lastActivity = dict["lastActivity"]
        room.created = dict["created"]
        return room
    fromDictionary = staticmethod(fromDictionary)


class SparkMessage:
    id = None
    roomId = None
    text = None
    personId = None
    personEmail = None
    created = None

    def __init__(self):
        pass

    def fromDictionary(dict):
        '''Creates a SparkMessage according to the dictionary given. Typically,
         this dictionary comes from a JSON object given by the Spark API'''
        message = SparkMessage()
        message.id = dict["id"],
        message.roomId = dict["roomId"],
        message.text = dict["text"],
        message.personId = dict["personId"],
        message.personEmail = dict["personEmail"],
        message.created = dict["created"]
        return message
    fromDictionary = staticmethod(fromDictionary)


class Spark:
    def __init__(self):
        pass

    def using(bearer):
        '''Initialises an instance of the Spark library with the given bearer
         token'''
        return SparkFacilitator(bearer)
    using = staticmethod(using)


class SparkFacilitator:
    __bearer = None

    def __init__(self, bearer):
        self.__bearer = bearer

    def room(self, room=None):
        '''Finds an instance of a Spark room with the given id'''
        if (isinstance(room, SparkRoom)):
            room = room.id
        return SparkRoomFacilitator(self.__bearer, room)

    def rooms(self, type=None):
        '''Lists the Spark rooms for a given user (according to the bearer
         token). Provide a type param of SparkRoom.DIRECT to only list 1:1
         rooms or SparkRoom.GROUP to only list group rooms'''
        return SparkRoomsFacilitator(self.__bearer, type)


class SparkRoomFacilitator:
    __bearer = None
    __id = None

    def __init__(self, bearer, id):
        self.__bearer = bearer
        self.__id = id

    def get(self):
        '''Retrieves an instance of a Spark room'''
        if (self.__id is None):
            raise AssertionError("Room id is required for a get(). Did you " +
                                 "forget 'id' in " +
                                 "Spark.using(xyz).room(id).get()?")
        headers = {"Authorization": "Bearer " + self.__bearer}
        response = requests.get(
            "https://api.ciscospark.com/v1/rooms/" + self.__id,
            headers=headers
        )
        return SparkRoom.fromDictionary(response.json())

    def create(self, title=None):
        '''Creates a new Spark room. Use title to set the title for the new
         room'''
        payload = {}
        if (title is not None):
            payload["title"] = title

        headers = {"Authorization": "Bearer " + self.__bearer}
        response = requests.post(
            "https://api.ciscospark.com/v1/rooms",
            json=payload,
            headers=headers
        )
        if (response.status_code == requests.codes.ok):
            return SparkRoom.fromDictionary(response.json())
        else:
            # expose the status code so this can be debugged
            return False

    def messages(self):
        '''Finds the messages associated with a Spark room'''
        return SparkMessagesFacilitator(self.__bearer, self.__id)

    def message(self, text=None, files=None):
        '''Creates a new message for a Spark room. Use text to send a text based
         message, files to send a file based message or both to send text and
         files'''
        return SparkMessageFacilitator(self.__bearer, self.__id, text, files)


class SparkMessagesFacilitator:
    __bearer = None
    __roomId = None

    def __init__(self, bearer, roomId):
        self.__bearer = bearer
        self.__roomId = roomId

    def get(self, before=None, beforeMessage=None, max=None):
        '''Retrieves the messages associated with a room. Use before with an
         ISO8601 format date to get messages before a certain time. Use
         beforeMessage with a message ID to retrieve messages before a certain
         message. Use max to limit the number of messages returned'''
        params = {"roomId": self.__roomId}
        if (before is not None):
            params["before"] = before
        if (beforeMessage is not None):
            params["beforeMessage"] = beforeMessage
        if (max is not None):
            params["max"] = max

        headers = {"Authorization": "Bearer " + self.__bearer}
        response = requests.get(
            "https://api.ciscospark.com/v1/messages",
            params=params,
            headers=headers
        )

        content = response.json()["items"]
        messages = []
        for message in content:
            messages.append(SparkMessage.fromDictionary(message))
        return messages


class SparkMessageFacilitator:
    __bearer = None
    __roomId = None
    __text = None
    __files = None

    def __init__(self, bearer, roomId, text=None, files=None):
        self.__bearer = bearer
        self.__roomId = roomId
        self.__text = text
        self.__files = files

    def post(self):
        '''Posts a message to a Spark room'''
        payload = {"roomId": self.__roomId}
        if (self.__text is not None):
            payload["text"] = self.__text
        if (self.__files is not None):
            payload["files"] = self.__files

        headers = {"Authorization": "Bearer " + self.__bearer}
        response = requests.post(
            "https://api.ciscospark.com/v1/messages",
            json=payload,
            headers=headers
        )
        return response.status_code == requests.codes.ok


class SparkRoomsFacilitator:
    __bearer = None
    __type = None

    def __init__(self, bearer, type=None):
        self.__bearer = bearer
        self.__type = type

    def get(self, max=None):
        '''Retrieves a list of Spark rooms associated with a user (according)
         to the bearer token given. Use max to limit the number of rooms
         returned'''
        params = {}
        if (self.__type is not None):
            params["type"] = self.__type
        if (max is not None):
            params["max"] = max

        headers = {"Authorization": "Bearer " + self.__bearer}
        response = requests.get(
            "https://api.ciscospark.com/v1/rooms",
            params=params,
            headers=headers
        )

        content = response.json()["items"]
        rooms = []
        for room in content:
            rooms.append(SparkRoom.fromDictionary(room))
        return rooms
