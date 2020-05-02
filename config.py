import constants as c

rows = 20
cols = 40
gameConfig = {
    "frameDelay": 1 / 60,
    "rows": rows,
    "cols": cols,
    "bgcolor": c.BG_COLOR_BLACK,
    "userInputKeys": {
        "exitKey": "escape",
        "playerLeftKey": "left",
        "playerRightKey": "right",
        "playerFireKey": "space"
    },
    "actors": {
        "gun-bullet": {
            "tag": "gun-bullet",
            "components": {
                "Velocity": { "rowVel": -1 },
                "VerticalBounds": {
                    "minRow": 0, 
                    "maxRow": rows - 2,
                    "onMinActions": [
                        { 'name': 'removeActor', 'params': 'self' },
                    ] 
                },
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_YELLOW + "|" + c.RESET]
                ]}
            }
        },
        "gun": {
            "tag": "gun",
            "row": float(rows - 1), "col": float(cols / 2),
            "components": {
                "ControlledByUser": { "moveLeftInputIndex": 1, "moveRightInputIndex": 2},
                "HorizontalBounds": { "minCol": 1, "maxCol": cols - 4 },
                "FireController": {
                    "ammoCapacity": 1,
                    "ammo": 1,
                    "rowOffset": -1,
                    "colOffset": 1,
                    "bullet": "gun-bullet",
                },
                "GunRender": { "sprite": [ 
                    [c.BOLD + c.FG_COLOR_GREEN + "╔", "╧", "╗" + c.RESET], 
                    [         c.FG_COLOR_GREEN + "╔", "═", "╗" + c.RESET] 
                ]}
            },
        },
        "alien": {
            "tag": "alien",
            "components": {
                "Velocity": { "colVel": 0.0, "rowVel": 0.0 },
                "HorizontalBounds": {"minCol": 1, "maxCol": cols - 4 },
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_CYAN + "╒", "H", "╕" + c.RESET], 
                    [c.BOLD + c.FG_COLOR_CYAN + "╘", "H", "╛" + c.RESET]
                ], "frame": 0}
            }
        }
    },
    "scene": {
        "description": "GAMEPLAY",
        "initialActors": {
            "gun": {},
            "alienArmy": {
                "tag": "alien-army",
                "components": {
                   "AlienArmyController": {
                        "actor": "alien",
                        "vel": 1.0 / 20.0,
                        "rows": 4,
                        "perRow": 8,
                        "step": 4,
                        "initialRow": 1,
                        "initialCol": 5
                   } 
                }
            }
        },
    }
}
   
