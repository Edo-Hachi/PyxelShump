# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Game
```bash
python main.py
```

### Prerequisites
- Python 3.7 or higher
- Pyxel game engine: `pip install pyxel`

### Virtual Environment
The project includes a `venv/` directory. Activate it with:
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

## Code Architecture

### Core Structure
This is a 2D shoot-em-up game built with the Pyxel game engine featuring:

- **Main Game Loop**: `main.py` - Contains the main `App` class with game states (Title, Playing, Game Over)
- **Global State Management**: `Common.py` - Centralized game state, constants, collision detection, and sprite management
- **Entity System**: Object-oriented approach with separate classes for game entities

### Key Components

#### Game States
- `STATE_TITLE`: Title screen with star field background
- `STATE_PLAYING`: Main gameplay with sub-states for enemy spawning, fighting, and stage clear
- `STATE_GAMEOVER`: Game over screen
- `STATE_PAUSE`: Pause functionality

#### Entity Classes
- **Player** (`Player.py`): Player ship with movement, shooting, collision, and invincibility mechanics
- **Enemy** (`Enemy.py`): Enemy entities with AI, group movement, multi-stage attack behavior, and shooting patterns
- **Bullet** (`Bullet.py`): Player projectiles
- **EnemyBullet** (`EnemyBullet.py`): Enemy projectiles
- **ExplodeManager** (`ExplodeManager.py`): Particle system for explosions
- **StarManager** (`StarManager.py`): Background star field animation

#### Core Game Systems
- **Collision Detection**: AABB collision system in `Common.check_collision()`
- **Stage Management**: 4 stages with different enemy spawn patterns defined in `Common.py`
- **Group Enemy Movement**: Enemies move as a cohesive group with direction changes at screen edges
- **Multi-Stage Enemy Attack System**: Enemies can transition between formation movement and individual attack behavior
- **Hit Effects**: Screen shake, hit-stop timing, and particle explosions
- **Scoring System**: Points awarded for enemy destruction

### Important Constants & Configuration

#### Game Settings
- Window size: 128x128 pixels
- Frame rate: 60 FPS  
- Display scale: 5x
- Sprite banks: 0, 1, 2

#### Sprite Management
- Sprites defined in `Common.SprList` dictionary using `SpIdx` namedtuple
- Enemy sprites support 4-frame animation cycles
- `get_enemy_sprite()` function handles sprite indexing for 5 enemy types

#### Stage Data
- Enemy spawn patterns stored as 10x4 grids in `ENEMY_MAP_STG01` through `ENEMY_MAP_STG04`
- Numbers 1-5 represent different enemy types
- `get_current_stage_map()` returns appropriate pattern for current stage

### Audio Resources
- Sound effects stored in `my_resource.pyxres` Pyxel resource file
- Channel 0 used for player shooting and enemy destruction sounds

### Enemy Attack System
The game features a sophisticated multi-stage enemy attack system with the following states:

#### Attack States
- **NORMAL** (0): Standard formation movement with the group
- **PREPARE_ATTACK** (1): Pre-attack preparation with visual shaking effects
- **ATTACK** (2): Individual attack descent with swaying movement
- **RETURNING** (3): Waiting state at screen bottom before returning
- **DESCENDING** (4): Returning to formation position

#### Attack Mechanics
- Enemies break formation individually to perform attack dives
- Preparation phase includes visual feedback (shaking) to telegraph attacks
- Attack descent features swaying movement for dynamic challenge
- Enemies return to formation after completing attack runs
- Cooldown system prevents immediate repeat attacks

#### Configuration Constants
- `PREPARE_ATTACK_DURATION`: 180 frames (3 seconds) preparation time
- `ATTACK_MOVE_SPEED`: 0.8 pixels per frame descent speed
- `ATTACK_SWAY_AMPLITUDE`: 1.5 pixels left-right sway range
- `RETURN_DELAY`: 120 frames (2 seconds) before returning
- `ATTACK_COOLDOWN`: 300 frames (5 seconds) post-attack cooldown

### Debug Features
- `Common.DEBUG` flag enables collision box visualization
- Green boxes for player, red boxes for enemies when enabled

## Development Notes

### Code Style
- Japanese comments mixed with English
- Global state management through `Common.py` module
- Entity lists stored globally: `enemy_list`, `player_bullet_list`, `enemy_bullet_list`

### Game Balance
- Enemy shooting probability increases as fewer enemies remain
- Player has invincibility frames after being hit with visual feedback
- Screen shake and hit-stop effects for impact feedback
- Enemy attack behavior includes preparation phase with visual feedback (shaking)
- Multi-stage enemy attack patterns with formation breaking and returning

### Resource Management
- Automatic garbage collection of inactive bullets and enemies
- Particle system manages explosion effects independently
- Virtual environment included for dependency isolation