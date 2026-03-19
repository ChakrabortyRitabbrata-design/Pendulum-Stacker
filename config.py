# config.py
WIDTH, HEIGHT = 800, 600
FPS = 60

# Physics
GRAVITY = 900.0
FRICTION = 0.8
ELASTICITY = 0.1
DAMPING = 0.5        # High damping = thick air (less swinging)

# Crane & Rope
ROPE_LENGTH = 150    # How long the string is
CRANE_SPEED = 10     # How fast you move the top anchor

# Wind
WIND_STRENGTH = 1200.0 # High because it has to push a heavy crane
WIND_CHANGE_TIME = 4.0

# Visuals
BLOCK_SIZE = (100, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 240, 255)      # Neon Cyan
RED = (255, 0, 85)        # Neon Pink
DARK_BG = (10, 10, 15)    # Dark background
GLASS_BG = (30, 30, 45, 150) # Semi-transparent
TEXT_COLOR = (240, 240, 240)