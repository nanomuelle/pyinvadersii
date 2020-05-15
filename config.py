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
                    "size": (0.4, 0.4),
                    "vel": (0, -10),
                    "minY": 0,
                    "collisionGroup": "gun-bullet",
                    "collidesWith": ["alien", "shield", "ufo", "alien-bullet"]
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
                    "size": (0.4, 0.4),
                    "vel": (0, 5),
                    "maxY": rows,
                    "collisionGroup": "alien-bullet",
                    "collidesWith": ["shield"]
                },
                "BulletController": {},
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_MAGENTA + "|" + c.RESET]
                ]}
            }
        },
        "gun": {
            "tag": "gun",
            "components": {
                "Transform": {"pos": (cols / 2, rows - 0.5)},
                "ControlledByUser": { "vel": 20.0 },
                "Physics": {
                    "size": (3.0, 1.0),
                    "vel": (0.0, 0.0),
                    "minX": 1.5,
                    "maxX": cols - 1.5,
                    "collisionGroup": "gun",
                    "collidesWith": ["alien-bullet"]
                },
                "FireController": {
                    "ammoCapacity": 1,
                    "ammo": 1,
                    "rowOffset": -1,
                    "colOffset": 0,
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
                    "maxX": cols - 4,
                    "collisionGroup": "alien",
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
        "explosion": {
            "tag": "explosion",
            "components": {
                "Transform": {"pos": (-1000, -1000)},
                "ExplosionController": { "duration": 0.3 },
                "AnsiRender": {
                    "animationTime": 0.3 / 3, 
                    "sprite": [
                        [c.FG_COLOR_RED + "X" + c.RESET],
                        [c.FG_COLOR_RED + "+" + c.RESET],
                        [c.FG_COLOR_RED + "." + c.RESET]
                    ]
                }
            }
        },
        "ufo": {
            "tag": "ufo",
            "components": {
                "Transform": {"pos": (cols + 4.0, 1.5)},
                "Physics": {
                    "size": (4.0, 1.0),
                    "vel": (-20.0, 0.0),
                    "minX": -4.0,
                    "maxX": cols + 4.0,
                    "collisionGroup": "ufo",
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
                "Physics": {
                    "size": (1.0, 1.0),
                    "collisionGroup": "shield",
                },
                "ShieldController": {
                    "maxDamage": 4,
                    # "onMaxDamageActions": [
                    #     {'name': 'removeActor', 'params': 'self'},
                    # ]
                },
                "AnsiRender": {"sprite": [
                    [c.BOLD + c.FG_COLOR_BLUE 
                                        + "█" + c.RESET],
                    [c.BOLD + c.FG_COLOR_BLUE +
                        c.BG_COLOR_MAGENTA + "▓" + c.RESET],
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLUE + "▒" + c.RESET],
                    [c.BOLD + c.FG_COLOR_MAGENTA +
                        c.BG_COLOR_BLACK + "░" + c.RESET],
                    [" "]
                ]}
            }
        },
        "score": {
            "tag": "score",
            "row": 0,
            "col": cols - 13,
            "components": {
                "Transform": {"pos": (cols - 7.0, 0.0)},
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
                    "Transform": {"pos": (70.0, 1.5)},
                    "Physics": {"vel": (-40.0, 0.0), "minX": 0.5 + cols / 2},
                    "AnsiRender": {"sprite": [r" _, __,  _,  _, __,"]}
                }},
                {"components": {
                    "Transform": {"pos": (80.0, 2.5)},
                    "Physics": {"vel": (-40, 0), "minX": cols / 2},
                    "AnsiRender": {"sprite": [r"(_  |_) / \ / ` |_"]}
                }},
                {"components": {
                    "Transform": {"pos": (90.0, 3.5)},
                    "Physics": {"vel": (-40, 0), "minX": cols / 2},
                    "AnsiRender": {"sprite": [r", ) |   |~| \ , | "]}
                }},
                {"components": {
                    "Transform": {"pos": (100.0, 4.5)},
                    "Physics": {"vel": (-40, 0), "minX": 0.5 + cols / 2},
                    "AnsiRender": {"sprite": [r" ~  ~   ~ ~  ~  ~~~"]}
                }},

                {"components": {
                    "Transform": {"pos": (110, 5.5)},
                    "Physics": {"vel": (-40, 0), "minX": 0.5 + cols / 2},
                    "AnsiRender": {"sprite": [r"_ _, _ _,_  _, __, __, __,  _,"]}
                }},
                {"components": {
                    "Transform": {"pos": (120, 6.5)},
                    "Physics": {"vel": (-40, 0), "minX": cols / 2},
                    "AnsiRender": {"sprite": [r"| |\ | | / / \ | \ |_  |_) (_"]}
                }},
                {"components": {
                    "Transform": {"pos": (130, 7.5)},
                    "Physics": {"vel": (-40, 0), "minX": 0.5 + cols / 2},
                    "AnsiRender": {"sprite": [r"| | \| |/  |~| |_/ |   | \ , )"]}
                }},
                {"components": {
                    "Transform": {"pos": (140, 8.5)},
                    "Physics": {"vel": (-40, 0), "minX": cols / 2},
                    "AnsiRender": {"sprite": [r"~ ~  ~ ~   ~ ~ ~   ~~~ ~ ~  ~"]}
                }},
                {"components": {
                    "Transform": {"pos": (cols / 2, 100.5)},
                    "Physics": {"vel": (0, -30), "minY": 12.5},
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
                # gun
                {"template": "gun"},
                # level name
                {"components": {
                    "Transform": {"pos": (8.5, 0.0)},
                    "TextRender": {"text": "SPACE INVADERS"}
                }},
                # score
                {"template": "score"},
                # shields
                {"template": "shield", "components": {"Transform": {"pos": (9.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (6.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (7.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (8.5, rows - 3.5)}}},

                {"template": "shield", "components": {"Transform": {"pos": (13.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (14.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (15.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (16.5, rows - 3.5)}}},

                {"template": "shield", "components": {"Transform": {"pos": (21.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (22.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (23.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (24.5, rows - 3.5)}}},

                {"template": "shield", "components": {"Transform": {"pos": (29.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (30.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (31.5, rows - 3.5)}}},
                {"template": "shield", "components": {"Transform": {"pos": (32.5, rows - 3.5)}}},
                # alienArmy"
                {"tag": "alien-army", "components": {
                    "AlienArmyController": {
                        "alienTag": "alien",
                        "explosionTag": "explosion",
                        # "ufoTag": "ufo",
                        "vel": 1.0,
                        "ivel": 0.2,
                        "rows": 4,
                        "perRow": 8,
                        "step": 4,
                        "initialRow": 2.5,
                        "initialCol": 5.5
                    }
                }},
                # Scene
                {"components": {
                    "ClasicScene": {
                        "lives": 3,
                        "alienArmyTag": "alien-army",
                        "playerTag": "gun"
                    }
                }}
            ],
        },
        {
            "description": "game over",
            "initialActors": [
                # GAME
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 1.5)},
                    "Physics": {"vel": (0, -10), "minY": 2.5 },
                    "AnsiRender": {"sprite": [" ██████╗  █████╗ ███╗   ███╗███████╗"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 2.5)},
                    "Physics": {"vel": (0, -10), "minY": 3.5 },
                    "AnsiRender": {"sprite": ["██╔════╝ ██╔══██╗████╗ ████║██╔════╝"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 3.5)},
                    "Physics": {"vel": (0, -10), "minY": 4.5 },
                    "AnsiRender": {"sprite": ["██║  ███╗███████║██╔████╔██║█████╗  "]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 4.5)},
                    "Physics": {"vel": (0, -10), "minY": 5.5 },
                    "AnsiRender": {"sprite": ["██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  "]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 5.5)},
                    "Physics": {"vel": (0, -10), "minY": 6.5 },
                    "AnsiRender": {"sprite": ["╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 6.5)},
                    "Physics": {"vel": (0, -10), "minY": 7.5},
                    "AnsiRender": {"sprite": [" ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"]}}},
                # OVER
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 12.5)},
                    "Physics": {"vel": (0, -10), "minY": 9.5},
                    "AnsiRender": {"sprite": [" ██████╗ ██╗   ██╗███████╗██████╗ "]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 13.5)},
                    "Physics": {"vel": (0, -10), "minY": 10.5},
                    "AnsiRender": {"sprite": ["██╔═══██╗██║   ██║██╔════╝██╔══██╗"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 14.5)},
                    "Physics": {"vel": (0, -10), "minY": 11.5},
                    "AnsiRender": {"sprite": ["██║   ██║██║   ██║█████╗  ██████╔╝"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 15.5)},
                    "Physics": {"vel": (0, -10), "minY": 12.5 },
                    "AnsiRender": {"sprite": ["██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗"]}}},
                {"row": rows + 16, "col": 2, "components": {
                    "Transform": {"pos": (cols / 2, rows + 16.5)},
                    "Physics": {"vel": (0, -10), "minY": 13.5 },
                    "AnsiRender": {"sprite": ["╚██████╔╝ ╚████╔╝ ███████╗██║  ██║"]}}},
                {"components": {
                    "Transform": {"pos": (cols / 2, rows + 17.5)},
                    "Physics": {"vel": (0, -10), "minY": 14.5},
                    "AnsiRender": {"sprite": [" ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝"]}}},

                {"components": {
                    "Transform": {"pos": (100, 17.5 )},
                    "Physics": {"vel": (-20, 0), "minX": cols / 2},
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
