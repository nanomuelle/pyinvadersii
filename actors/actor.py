import sys

from .components.alienArmyControllerComponent import AlienArmyControllerComponent
from .components.ansiRenderComponent import AnsiRenderComponent
from .components.controlledByUserComponent import ControlledByUserComponent
from .components.fireControllerComponent import FireControllerComponent
from .components.followActorComponent import FollowActorComponent
from .components.gunRenderComponent import GunRenderComponent
from .components.horizontalBoundsComponent import HorizontalBoundsComponent
from .components.velocityComponent import VelocityComponent
from .components.verticalBoundsComponent import VerticalBoundsComponent

ComponentFactory = {
    "AlienArmyController": AlienArmyControllerComponent,
    "AnsiRender": AnsiRenderComponent,
    "ControlledByUser": ControlledByUserComponent,
    "FireController": FireControllerComponent,
    "FollowActor": FollowActorComponent,
    "GunRender": GunRenderComponent,
    "HorizontalBounds": HorizontalBoundsComponent,
    "Velocity": VelocityComponent,
    "VerticalBounds": VerticalBoundsComponent
}

def createActorComponent(componentName, actorId):
    Constructor = ComponentFactory.get(componentName, False)
    if not Constructor:
        print("ERROR: componente desconocido '{}'".format(componentName))
        sys.exit()
    component = Constructor(actorId)
    return component

def idGenerator(firstValue):
    id = firstValue
    while True:
        yield id
        id += 1

class Actor:
    actorIdGenerator = idGenerator(1)

    def __init__(self):
        self.id = next(Actor.actorIdGenerator)
        self.components = {}

    def init(self, game, cfg):
        # print("Actor.init id: {} cfg: {}".format(self.id, cfg))
        self.tag = cfg.get('tag', 'actor-{}'.format(self.id))
        self.game = game
        self.row = cfg.get('row', -1000)
        self.col = cfg.get('col', -1000)
        self.createComponents(cfg)

    def createComponents(self, cfg):
        for (componentName, componentCfg) in cfg['components'].items():
            component = createActorComponent(componentName, self.id)
            component.init(self.game, componentCfg)
            self.components[component.__class__.componentType] = component

    def getComponent(self, componentType):
        component = self.components.get(componentType, False)
        if not component:
            print("Error: {} component not found in actor {}".format(componentType, self))
            sys.exit()
        return component

    # def getCurrentSprite(self):
    #     return self.sprite[self.frame]

class BulletActor(Actor):
    def __init__(self, actorCfg):
        Actor.__init__(self)
        self.fired = actorCfg['fired']

# class GunActor(Actor):
#     def __init__(self, row, col, sprite, frame):
#         Actor.__init__(self, row, col, sprite, frame)

# class AlienActor(Actor):
#     def __init__(self, row, col, sprite, frame):
#         Actor.__init__(self, row, col, sprite, frame)    


