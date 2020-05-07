import constants as c

rows = 20
cols = 40
gameConfig = {
    "frameDelay": 1 / 30,
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
                "Physics": {"w": 1, "h": 1, "rowVel": -0.5},
                "VerticalBounds": {
                    "minRow": 0,
                    "maxRow": rows - 2,
                    "onMinActions": [
                        {'name': 'removeActor', 'params': 'self'},
                    ]
                },
                "AutodestroyCollision": {},
                "AnsiRender": {
                    "sprite": [
                        [c.BOLD + c.FG_COLOR_YELLOW + "|" + c.RESET]
                    ]
                }
            }
        },
        "alien-bullet": {
            "tag": "alien-bullet",
            "components": {
                "Physics": {"w": 1, "h": 1, "rowVel": 0.2},
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
                "Physics": {"w": 3, "h": 1},
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
                "Physics": {"w": 3, "h": 1},
                "HorizontalBounds": {"minCol": 1, "maxCol": cols - 4},
                "AlienController": {
                    "fireProb": 0.0005
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
        "ufo": {
            "tag": "ufo",
            "row": 1.0, "col": float(cols + 4),
            "components": {
                "Physics": {"w": 4, "h": 1, "colVel": -0.2 },
                "HorizontalBounds": { 
                    "minCol": -10, 
                    "maxCol": cols + 10,
                    "onMinActions": [{'name': 'removeActor', 'params': 'self'}],
                    "onMaxActions": [{'name': 'removeActor', 'params': 'self'}] 
                },
                "AnsiRender": { "sprite": [
                    [c.BOLD + c.FG_COLOR_RED + "(", "═", c.BLINK + "═", "═", ")" + c.RESET]
                ]}
            }
        },
        "shield": {
            "tag": "shield",
            "row": rows - 4,
            "col": 0,
            "components": {
                "Physics": {"w": 1, "h": 1},
                "ShieldController": {
                    "maxDamage": 4,
                    "damage": 0,
                    "onMaxDamageActions": [
                        {'name': 'removeActor', 'params': 'self'},
                    ]
                },
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLUE + "█" + c.RESET],
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLUE + "▓" + c.RESET],
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLUE + "▒" + c.RESET],
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLUE + "░" + c.RESET],
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
        },
        "vscroll-text": {
            "tag": "vscroll-text",
            "components": {
                "Physics": {"rowVel": -0.1}
            }
        },
    },
    "scenes": [
        {
            "description": "MAIN MENU",
            "initialActors": [
                # title
                {"row": 1, "col": 70, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 11, "maxCol": 100},
                    "AnsiRender": {"sprite": [r" _, __,  _,  _, __,"]}
                }},
                {"row": 2, "col": 80, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 11, "maxCol": 100},
                    "AnsiRender": {"sprite": [r"(_  |_) / \ / ` |_"]}
                }},
                {"row": 3, "col": 90, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 11, "maxCol": 100},
                    "AnsiRender": {"sprite": [r", ) |   |~| \ , | "]}
                }},
                {"row": 4, "col": 100, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 11, "maxCol": 100},
                    "AnsiRender": {"sprite": [r" ~  ~   ~ ~  ~  ~~~"]}
                }},

                {"row": 5, "col": 110, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 5, "maxCol": 140},
                    "AnsiRender": {"sprite": [r"_ _, _ _,_  _, __, __, __,  _,"]}
                }},
                {"row": 6, "col": 120, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 5, "maxCol": 140},
                    "AnsiRender": {"sprite": [r"| |\ | | / / \ | \ |_  |_) (_"]}
                }},
                {"row": 7, "col": 130, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 5, "maxCol": 140},
                    "AnsiRender": {"sprite": [r"| | \| |/  |~| |_/ |   | \ , )"]}
                }},
                {"row": 8, "col": 140, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 5, "maxCol": 140},
                    "AnsiRender": {"sprite": [r"~ ~  ~ ~   ~ ~ ~   ~~~ ~ ~  ~"]}
                }},
                {"row": 100, "col": 9, "components": {
                    "Physics": {"rowVel": -1.5},
                    "VerticalBounds": {"minRow": 12, "maxRow": 500},
                    "AnsiRender": {
                        "sprite": [
                            [c.BOLD + c.BG_COLOR_MAGENTA + "P", "R", "E", "S", "S", " ",
                             "A", "N", "Y", " ", "K", "E", "Y", " ", "T", "O", " ",
                             "S", "T", "A", "R", "T" + c.RESET]
                        ]
                    }}
                },
                {
                    "components": {
                        "IntroScene" : {}
                    }
                }
            ]
        },
        {
            "description": "GAMEPLAY",
            "initialActors": [
                # level name
                {"row": 0, "col": 1, "components": {
                    "TextRender": {"text": "SPACE INVADERS"}
                }},
                # score
                {"template": "score"},
                # shields
                {"template": "shield", "col": 6},
                {"template": "shield", "col": 7},
                {"template": "shield", "col": 8},
                {"template": "shield", "col": 9},

                {"template": "shield", "col": 14},
                {"template": "shield", "col": 15},
                {"template": "shield", "col": 16},
                {"template": "shield", "col": 17},

                {"template": "shield", "col": 22},
                {"template": "shield", "col": 23},
                {"template": "shield", "col": 24},
                {"template": "shield", "col": 25},

                {"template": "shield", "col": 30},
                {"template": "shield", "col": 31},
                {"template": "shield", "col": 32},
                {"template": "shield", "col": 33},
                # gun
                {"template": "gun"},
                # alienArmy"
                {"tag": "alien-army", "components": {
                    "AlienArmyController": {
                        "alienTag": "alien",
                        "ufoTag": "ufo",
                        "vel": 1.0 / 60.0,
                        "ivel": 1.0 / 80.0,
                        "rows": 4,
                        "perRow": 8,
                        "step": 4,
                        "initialRow": 2,
                        "initialCol": 5
                    }
                }},
                {
                    "components": {
                        "ClasicScene": {
                            "lives": 3,
                            "alienArmyTag": "alien-army" 
                        }
                    }
                }
            ],
        },
        {
            "description": "game over",
            "initialActors": [
                {"row": rows + 1, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 2, "maxRow": 100},
                    "AnsiRender": {"sprite": [" ██████╗  █████╗ ███╗   ███╗███████╗"]}}},
                {"row": rows + 2, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 3, "maxRow": 100},
                    "TextRender": {"text": "██╔════╝ ██╔══██╗████╗ ████║██╔════╝"
                                   }}},
                {"row": rows + 3, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 4, "maxRow": 100},
                    "TextRender": {"text": "██║  ███╗███████║██╔████╔██║█████╗  "
                                   }}},
                {"row": rows + 4, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 5, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  "
                                   }}},
                {"row": rows + 5, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 6, "maxRow": 100},
                    "TextRender": {"text": "╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗"
                                   }}},
                {"row": rows + 6, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 7, "maxRow": 100},
                    "TextRender": {"text": " ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"
                                   }}},

                {"row": rows + 12, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 8, "maxRow": 100},
                    "TextRender": {"text": " ██████╗ ██╗   ██╗███████╗██████╗ "}}},
                {"row": rows + 13, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 9, "maxRow": 100},
                    "TextRender": {"text": "██╔═══██╗██║   ██║██╔════╝██╔══██╗"
                                   }}},
                {"row": rows + 14, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 10, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║██║   ██║█████╗  ██████╔╝"
                                   }}},
                {"row": rows + 15, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 11, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗"
                                   }}},
                {"row": rows + 16, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 12, "maxRow": 100},
                    "TextRender": {"text": "╚██████╔╝ ╚████╔╝ ███████╗██║  ██║"
                                   }}},
                {"row": rows + 17, "col": 2, "components": {
                    "Physics": {"rowVel": -0.1},
                    "VerticalBounds": {"minRow": 13, "maxRow": 100},
                    "TextRender": {"text": " ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝"
                                   }}},

                {"row": 15, "col": 500, "components": {
                    "Physics": {"colVel": -2},
                    "HorizontalBounds": {"minCol": 12, "maxCol": 500},
                    "AnsiRender": {
                        "sprite": [
                            [c.BOLD + c.BG_COLOR_MAGENTA + "[", "E", "S", "C", "]", " ",
                             "E", "x", "i", "t", " ", "g", "a", "m", "e" + c.RESET]
                        ]
                    }}}
            ]
        },
    ]
}

# 1      _, __,  _,  _, __,
# 2     (_  |_) / \ / ` |_
# 3     , ) |   |~| \ , |
# 4      ~  ~   ~ ~  ~  ~~~
#
# 1 _ _, _ _,_  _, __, __, __,  _,
# 2 | |\ | | / / \ | \ |_  |_) (_
# 3 | | \| |/  |~| |_/ |   | \ , )
# 4 ~ ~  ~ ~   ~ ~ ~   ~~~ ~ ~  ~


# 1  ██████╗  █████╗ ███╗   ███╗███████╗
# 2 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
# 3 ██║  ███╗███████║██╔████╔██║█████╗
# 4 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
# 5 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
# 6  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝

# 1  ██████╗ ██╗   ██╗███████╗██████╗
# 2 ██╔═══██╗██║   ██║██╔════╝██╔══██╗
# 3 ██║   ██║██║   ██║█████╗  ██████╔╝
# 4 ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
# 5 ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
# 6  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
