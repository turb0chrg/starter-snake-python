import json
import os
import random
import logging

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "nibblesreturns is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    #Wren
    response = { 
        "color": "#c20893",
        "headType": "safe",
        "tailType": "curled"
    }

    #Reid
    # response = {
    #     "color": "#171716",
    #     "headType": "sand-worm",
    #     "tailType": "curled"
    # }

    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))

    #Other snakes
    # for x in data["board"]["snakes"]:
    #     print ( x["name"]  )
    #     print ( "shouts" )
    #     print ( x["shout"] )

    logging.warning('And this, too')
    
    #Useful board dynamic references 
    height = data["board"]["height"] - 1
    width = data["board"]["width"] - 1

    #Useful self dynamic references
    body = data["you"]["body"]
    head = body[0]

    print ("my head is at", head)

    print ("height:", height)
    print ("width:", width)

    #Starting direction list, we'll be eliminating directions as we go
    direction = ["up", "down", "left", "right"]

    #Deal with collisions
    for segment in body:
        if (head["x"] == segment["x"] + 1 and head["y"] == segment["y"]): #segment left of head 
            direction.remove("left")
        if (head["x"] == segment["x"] - 1 and head["y"] == segment["y"]): #segment right of head
            direction.remove("right")
        if (head["y"] == segment["y"] + 1 and head["x"] == segment["x"]): #segment up from head
            direction.remove("up")
        if (head["y"] == segment["y"] - 1 and head["x"] == segment["x"]): #segment down from head
            direction.remove("down")

    #Deal with walls (doesn't deal with corner cases)
    if head["x"] == 0: #left board
        direction.remove("left")
    
    if head["x"] == width: #right board
        direction.remove("right")
    
    if head["y"] == 0: #top board
        direction.remove("up")
    
    if head["y"] == height: #bottom board
        direction.remove("down")
    
    print ( direction )
    
    move = random.choice(direction) # Choose a random direction to move in

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "1991 is calling: I am a decendant of QBasic Nibbles"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    #print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    #logging.basicConfig(filename='battlesnake.log',level=logging.DEBUG)

    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
        #reloader=True,
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
