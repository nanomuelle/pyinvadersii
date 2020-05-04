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
                "Velocity": {"rowVel": -0.5},
                "VerticalBounds": {
                    "minRow": 0,
                    "maxRow": rows - 2,
                    "onMinActions": [
                        {'name': 'removeActor', 'params': 'self'},
                    ]
                },
                "AutodestroyCollision": {},
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_YELLOW + "|" + c.RESET]
                ]}
            }
        },
        "alien-bullet": {
            "tag": "alien-bullet",
            "components": {
                "Velocity": {"rowVel": 0.2},
                "VerticalBounds": {
                    "minRow": 0,
                    "maxRow": rows,
                    "onMaxActions": [
                        {'name': 'removeActor', 'params': 'self'},
                    ]
                },
                "AutodestroyCollision": {},
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_CYAN + "╎" + c.RESET]
                ]}
            }
        },
        "gun": {
            "tag": "gun",
            "row": float(rows - 1), "col": float(cols / 2),
            "components": {
                "ControlledByUser": {"moveLeftInputIndex": 1, "moveRightInputIndex": 2},
                "HorizontalBounds": {"minCol": 1, "maxCol": cols - 4},
                "FireController": {
                    "ammoCapacity": 1,
                    "ammo": 1,
                    "rowOffset": -1,
                    "colOffset": 1,
                    "bullet": "gun-bullet",
                },
                "GunRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_GREEN + "╔", "╧", "╗" + c.RESET],
                    [c.FG_COLOR_GREEN + "╔", "═", "╗" + c.RESET]
                ]}
            },
        },
        "alien": {
            "tag": "alien",
            "components": {
                "Velocity": {"colVel": 0.0, "rowVel": 0.0},
                "HorizontalBounds": {"minCol": 1, "maxCol": cols - 4},
                "AlienController": {
                    "fireProb": 0.001
                },
                "FireController": {
                    "ammoCapacity": 1,
                    "ammo": 1,
                    "rowOffset": 1,
                    "colOffset": 1,
                    "bullet": "alien-bullet",
                },
                "AlienRender": {
                    "sprite": [
                        [c.FG_COLOR_CYAN + "╒", "H", "╕" + c.RESET],
                        [c.FG_COLOR_CYAN + "╘", "H", "╛" + c.RESET]
                    ],
                    "frame": 0
                }
            }
        },
        "shield": {
            "tag": "shield",
            "row": rows - 4,
            "col": 0,
            "components": {
                "ShieldController": {
                    "maxDamage": 4,
                    "damage": 0, 
                    "onMaxDamageActions": [
                        {'name': 'removeActor', 'params': 'self'},
                    ]
                },
                "AnsiRender": {"sprite": [
                    # [c.BOLD + c.FG_COLOR_GREEN + "4" + c.RESET],
                    # [c.BOLD + c.FG_COLOR_GREEN + "3" + c.RESET],
                    # [c.BOLD + c.FG_COLOR_GREEN + "2" + c.RESET],
                    # [c.BOLD + c.FG_COLOR_GREEN + "1" + c.RESET],
                    # ["0"],
                    [c.BOLD + c.FG_COLOR_GREEN + "█" + c.RESET],
                    [c.BOLD + c.FG_COLOR_GREEN + "▓" + c.RESET],
                    [c.BOLD + c.FG_COLOR_GREEN + "▒" + c.RESET],
                    [c.BOLD + c.FG_COLOR_GREEN + "░" + c.RESET],
                    [" "]
                ]}
            }
        },
        "score": {
            "tag": "score",
            "row": 0,
            "col": cols - 13,
            "components": {
                "ScoreController": {
                    "pointsPerAlien": 10,
                },
                "TextRender": {
                    "text": "SCORE:{}",
                    "value": '000000'
                }
            }
        }
    },
    "scene": {
        "description": "GAMEPLAY",
        "initialActors": [
            # level name
            { "row": 0, "col": 1, "components": {
                "TextRender": {"text": "SPACE INVADERS"}
            }},
            # score
            { "template": "score" },
            # shields
            { "template": "shield", "col": 6 },
            { "template": "shield", "col": 7 },
            { "template": "shield", "col": 8 },
            { "template": "shield", "col": 9 },

            { "template": "shield", "col": 14 },
            { "template": "shield", "col": 15 },
            { "template": "shield", "col": 16 },
            { "template": "shield", "col": 17 },

            { "template": "shield", "col": 22 },
            { "template": "shield", "col": 23 },
            { "template": "shield", "col": 24 },
            { "template": "shield", "col": 25 },

            { "template": "shield", "col": 30 },
            { "template": "shield", "col": 31 },
            { "template": "shield", "col": 32 },
            { "template": "shield", "col": 33 },
            # gun
            { "template": "gun"},
            # alienArmy"
            { "tag": "alien-army", "components": {
                "AlienArmyController": {
                    "actor": "alien",
                    "vel": 1.0 / 20.0,
                    "ivel": 1.0 / 80.0,
                    "rows": 4,
                    "perRow": 8,
                    "step": 4,
                    "initialRow": 2,
                    "initialCol": 5
                }
            }}
        ],
    }
}