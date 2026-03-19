# physics_engine.py
import pymunk
from config import *

class PhysicsWorld:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)
        self.space.damping = 0.95 # Prevents infinite swinging
        
        # 1. The Floor
        floor_body = self.space.static_body
        floor_shape = pymunk.Segment(floor_body, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 5)
        floor_shape.friction = 1.0
        self.space.add(floor_shape)
        
        # 2. The Anchor (The top of the rope - controlled by player)
        self.anchor_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.anchor_body.position = (WIDTH // 2, 0)
        
        # 3. The Crane Head (The red box that swings)
        mass = 5.0 # Heavier crane makes for more stable swinging
        moment = pymunk.moment_for_box(mass, (100, 20))
        self.crane_body = pymunk.Body(mass, moment)
        self.crane_body.position = (WIDTH // 2, ROPE_LENGTH)
        self.crane_shape = pymunk.Poly.create_box(self.crane_body, (100, 20))
        self.crane_shape.friction = 0.5
        # Prevent crane from colliding with the blocks it drops
        self.crane_shape.filter = pymunk.ShapeFilter(group=1)
        
        # 4. The Joint (The String)
        self.joint = pymunk.PinJoint(self.anchor_body, self.crane_body, (0,0), (0,0))
        
        self.space.add(self.crane_body, self.crane_shape, self.joint)
        self.blocks = []

    def create_block(self, pos, velocity):
        mass = 1.0
        moment = pymunk.moment_for_box(mass, BLOCK_SIZE)
        body = pymunk.Body(mass, moment)
        body.position = pos
        # Important: The block inherits the swinging speed of the crane!
        body.velocity = velocity 
        
        shape = pymunk.Poly.create_box(body, BLOCK_SIZE)
        shape.friction = FRICTION
        shape.elasticity = ELASTICITY
        self.space.add(body, shape)
        self.blocks.append(shape)

    def update(self, dt):
        self.space.step(dt)