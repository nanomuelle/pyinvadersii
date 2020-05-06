import sys

from .components.alienArmyControllerComponent import AlienArmyControllerComponent
from .components.alienControllerComponent import AlienControllerComponent
from .components.alienRenderComponent import AlienRenderComponent
from .components.ansiRenderComponent import AnsiRenderComponent
from .components.autodestroyCollisionComponent import AutodestroyCollisionComponent
from .components.clasicSceneComponent import ClasicSceneComponent
from .components.controlledByUserComponent import ControlledByUserComponent
from .components.fireControllerComponent import FireControllerComponent
from .components.followActorComponent import FollowActorComponent
from .components.gunRenderComponent import GunRenderComponent
from .components.horizontalBoundsComponent import HorizontalBoundsComponent
from .components.introSceneComponent import IntroSceneComponent
from .components.physicsComponent import PhysicsComponent
from .components.scoreControllerComponent import ScoreControllerComponent
from .components.shieldControllerComponent import ShieldControllerComponent
from .components.textRenderComponent import TextRenderComponent
# from .components.velocityComponent import VelocityComponent
from .components.verticalBoundsComponent import VerticalBoundsComponent

ComponentFactory = {
    "AlienArmyController": AlienArmyControllerComponent,
    "AlienController": AlienControllerComponent,
    "AlienRender": AlienRenderComponent,
    "AutodestroyCollision": AutodestroyCollisionComponent,
    "AnsiRender": AnsiRenderComponent,
    "ClasicScene": ClasicSceneComponent,
    "ControlledByUser": ControlledByUserComponent,
    "FireController": FireControllerComponent,
    "FollowActor": FollowActorComponent,
    "GunRender": GunRenderComponent,
    "HorizontalBounds": HorizontalBoundsComponent,
    "IntroScene": IntroSceneComponent,
    "Physics": PhysicsComponent,
    "ScoreController": ScoreControllerComponent,
    "ShieldController": ShieldControllerComponent,
    "TextRender": TextRenderComponent,
    # "Velocity": VelocityComponent,
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
        self.oldPos = (-1000, -1000)
        self.pos = (cfg.get('row', -1000), cfg.get('col', -1000))
        self.createComponents(cfg)

    def setPos(self, row, col):
        self.oldPos = tuple(self.pos)
        self.pos = (row, col)

    @property
    def col(self):
        return self.pos[1]

    @property
    def row(self):
        return self.pos[0]

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