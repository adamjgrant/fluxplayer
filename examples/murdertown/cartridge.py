class Conversation():
    def __init__(self, namespace):
        self.namespace = namespace

    def dict(self):
        return {
            f"{self.namespace}_QUESTION1": {
                "prompt": "",
                "events": [
                    {
                        "target": "QUESTION2",
                        "if_the_user": ""
                    }
                ]
            }
        }


cartridge = {
    "START": {
        "role": "",
        "prompt": "",
        "events": [
            {
                "target": "NORTH_SIDE",
                "if_the_user": ""
            },
            {
                "target": "EAST_SIDE",
                "if_the_user": ""
            },
            {
                "target": "WEST_SIDE",
                "if_the_user": ""
            },
            {
                "target": "SOUTH_SIDE",
                "if_the_user": ""
            }
        ]
    }
}

cartridge = {**cartridge, **(Conversation("foo").dict())}

print(cartridge)
