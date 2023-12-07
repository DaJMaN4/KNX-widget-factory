import json
import yaml


class CreateSchematics:
    def __init__(self, main):
        self.main = main
        self.path = self.main.path
        self.create()

    def create(self):
        trendSchem = r"""
{
    "plan": {
        "background": "",
        "background_add": "",
        "bgcolor": "#E5E5E5",
        "bgfixed": 0,
        "bgrepeat": 0,
        "building": 0,
        "height": 555,
        "id": 55,
        "layout": 0,
        "locx": "",
        "locy": "",
        "name": "%roomName%",
        "objects": [
            {
                "cls": "",
                "floor": 55,
                "id": 2387,
                "locx": 1,
                "locy": 1,
                "name": "",
                "nobg": 1,
                "notouch": 0,
                "params": "{\"source\":\"url\",\"url\":\"\/scada-vis\/trends?id=%trendAddresses%&mode=day\",\"width\":\"1398\",\"height\":\"553\",\"refresh\":\"\",\"persist\":0}",
                "pincode": "",
                "type": 9
            }
        ],
        "pincode": "",
        "sortorder": 35,
        "touch_bgcolor": "",
        "touch_param": "",
        "type": "widget",
        "usermode_param": "",
        "width": 1400
    }
}
        """

        trendDict = json.loads(trendSchem)
        file = open(self.path + "/schematics/widgets/trends/default.yml", "x")
        yaml.dump(trendDict, file, allow_unicode=True)
