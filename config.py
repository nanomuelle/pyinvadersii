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
                "Transform": {},
                "Physics": {
                    "size": (1.0, 1.0),
                    "vel": (0, -20),
                    "minY": 0
                },
                "BulletController": {},
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
                "Transform": {},
                "Physics": {
                    "size": (1.0, 1.0),
                    "vel": (0, 10),
                    "maxY": rows
                },
                "BulletController": {},
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_CYAN + "╎" + c.RESET]
                ]}
            }
        },
        "gun": {
            "tag": "gun",
            "components": {
                "Transform": {"pos": (cols / 2, rows - 1)},
                "ControlledByUser": { "vel": 20.0 },
                "Physics": {
                    "size": (3.0, 1.0),
                    "vel": (0.0, 0.0),
                    "minX": 1,
                    "maxX": cols - 4
                },
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
                "Transform": {},
                "Physics": {
                    "size": (3.0, 1.0),
                    "minX": 1,
                    "maxX": cols - 4
                },
                "AlienController": {"fireProb": 0.0005},
                "FireController": {
                    "ammoCapacity": 1,
                    "ammo": 1,
                    "rowOffset": 1,
                    "colOffset": 1,
                    "bullet": "alien-bullet",
                },
                "AnsiRender": {
                    "sprite": [
                        [c.FG_COLOR_CYAN + "╒", "H", "╕" + c.RESET],
                        [c.FG_COLOR_CYAN + "╘", "H", "╛" + c.RESET]
                    ],
                    "frame": 0,
                    "animationTime": 0.5
                }
            }
        },
        "ufo": {
            "tag": "ufo",
            "row": 1.0, "col": float(cols + 4),
            "components": {
                "Transform": {"pos": (cols + 4, 1)},
                "Physics": {
                    "size": (4.0, 1.0),
                    "vel": (-20.0, 0.0),
                    "minX": -10.0,
                    "maxX": cols + 10.0
                },
                "UfoController": {},
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_RED +
                        "(", "═", "═", "═", ")" + c.RESET]
                ]}
            }
        },
        "shield": {
            "tag": "shield",
            "row": rows - 4,
            "col": 0,
            "components": {
                "Transform": {"pos": (0.0, rows - 4)},
                "Physics": {"size": (1.0, 1.0)},
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
                "Transform": {"pos": (cols - 13, 0.0)},
                "ScoreController": {"pointsPerAlien": 10},
                "TextRender": {
                    "text": "SCORE:{}",
                    "value": '000000'
                }
            }
        }
    },
    "scenes": [
        {
            "description": "MAIN MENU",
            "initialActors": [
                # title
                {"components": {
                    "Transform": {"pos": (70.0, 1.0)},
                    "Physics": {"vel": (-40.0, 0.0), "minX": 11.0},
                    "AnsiRender": {"sprite": [r" _, __,  _,  _, __,"]}
                }},
                {"components": {
                    "Transform": {"pos": (80, 2)},
                    "Physics": {"vel": (-40, 0), "minX": 11},
                    "AnsiRender": {"sprite": [r"(_  |_) / \ / ` |_"]}
                }},
                {"components": {
                    "Transform": {"pos": (90, 3)},
                    "Physics": {"vel": (-40, 0), "minX": 11},
                    "AnsiRender": {"sprite": [r", ) |   |~| \ , | "]}
                }},
                {"components": {
                    "Transform": {"pos": (100, 4)},
                    "Physics": {"vel": (-40, 0), "minX": 11},
                    "AnsiRender": {"sprite": [r" ~  ~   ~ ~  ~  ~~~"]}
                }},

                {"components": {
                    "Transform": {"pos": (110, 5)},
                    "Physics": {"vel": (-40, 0), "minX": 5},
                    "AnsiRender": {"sprite": [r"_ _, _ _,_  _, __, __, __,  _,"]}
                }},
                {"components": {
                    "Transform": {"pos": (120, 6)},
                    "Physics": {"vel": (-40, 0), "minX": 5},
                    "AnsiRender": {"sprite": [r"| |\ | | / / \ | \ |_  |_) (_"]}
                }},
                {"components": {
                    "Transform": {"pos": (130, 7)},
                    "Physics": {"vel": (-40, 0), "minX": 5},
                    "AnsiRender": {"sprite": [r"| | \| |/  |~| |_/ |   | \ , )"]}
                }},
                {"components": {
                    "Transform": {"pos": (140, 8)},
                    "Physics": {"vel": (-40, 0), "minX": 5},
                    "AnsiRender": {"sprite": [r"~ ~  ~ ~   ~ ~ ~   ~~~ ~ ~  ~"]}
                }},
                {"components": {
                    "Transform": {"pos": (9, 100)},
                    "Physics": {"vel": (0, -30), "minY": 12},
                    "AnsiRender": {
                        "sprite": [
                            [c.BOLD + c.BG_COLOR_MAGENTA + "P", "R", "E", "S", "S", " ",
                             "S", "P", "A", "C", "E", " ", "T", "O", " ",
                             "S", "T", "A", "R", "T" + c.RESET]
                        ]
                    }}
                 },

                # IntroScene
                {"components": {
                    "IntroScene": {}
                }}
            ]
        },
        {
            "description": "GAMEPLAY",
            "initialActors": [
                # level name
                {"components": {
                    "Transform": {"pos": (1.0, 0.0)},
                    "TextRender": {"text": "SPACE INVADERS"}
                }},
                # score
                {"template": "score"},
                # shields
                {"template": "shield", "components": {"Transform": {"pos": (10, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (7.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (8.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (9.0, rows - 4)}}},

                {"template": "shield", "components": {"Transform": {"pos": (14.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (15.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (16.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (17.0, rows - 4)}}},

                {"template": "shield", "components": {"Transform": {"pos": (22.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (23.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (24.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (25.0, rows - 4)}}},

                {"template": "shield", "components": {"Transform": {"pos": (30.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (31.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (32.0, rows - 4)}}},
                {"template": "shield", "components": {"Transform": {"pos": (33.0, rows - 4)}}},
                # gun
                {"template": "gun"},
                # alienArmy"
                {"tag": "alien-army", "components": {
                    "AlienArmyController": {
                        "alienTag": "alien",
                        # "ufoTag": "ufo",
                        "vel": 1.0,
                        "ivel": 0.2,
                        "rows": 4,
                        "perRow": 8,
                        "step": 4,
                        "initialRow": 2,
                        "initialCol": 5
                    }
                }},
                # Scene
                {"components": {
                    "ClasicScene": {
                        "lives": 3,
                        "alienArmyTag": "alien-army"
                    }
                }}
            ],
        },
        {
            "description": "game over",
            "initialActors": [
                {"components": {
                    "Transform": {"pos": (2.0, rows + 1.0)},
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 2, "maxRow": 100},
                    "AnsiRender": {"sprite": [" ██████╗  █████╗ ███╗   ███╗███████╗"]}}},
                {"row": rows + 2, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 3, "maxRow": 100},
                    "TextRender": {"text": "██╔════╝ ██╔══██╗████╗ ████║██╔════╝"
                                   }}},
                {"row": rows + 3, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 4, "maxRow": 100},
                    "TextRender": {"text": "██║  ███╗███████║██╔████╔██║█████╗  "
                                   }}},
                {"row": rows + 4, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 5, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  "
                                   }}},
                {"row": rows + 5, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 6, "maxRow": 100},
                    "TextRender": {"text": "╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗"
                                   }}},
                {"row": rows + 6, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 7, "maxRow": 100},
                    "TextRender": {"text": " ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"
                                   }}},

                {"row": rows + 12, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 8, "maxRow": 100},
                    "TextRender": {"text": " ██████╗ ██╗   ██╗███████╗██████╗ "}}},
                {"row": rows + 13, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 9, "maxRow": 100},
                    "TextRender": {"text": "██╔═══██╗██║   ██║██╔════╝██╔══██╗"
                                   }}},
                {"row": rows + 14, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 10, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║██║   ██║█████╗  ██████╔╝"
                                   }}},
                {"row": rows + 15, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 11, "maxRow": 100},
                    "TextRender": {"text": "██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗"
                                   }}},
                {"row": rows + 16, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 12, "maxRow": 100},
                    "TextRender": {"text": "╚██████╔╝ ╚████╔╝ ███████╗██║  ██║"
                                   }}},
                {"row": rows + 17, "col": 2, "components": {
                    "Physics": {"vel": (0, -10)},
                    "VerticalBounds": {"minRow": 13, "maxRow": 100},
                    "TextRender": {"text": " ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝"
                                   }}},

                {"row": 15, "col": 500, "components": {
                    "Physics": {"vel": (-20, 0)},
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
