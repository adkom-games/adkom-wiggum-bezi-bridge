## Roll-A-Ball Implementation Plan

### Executive Summary

**Project Goal:** Create a playable Roll-A-Ball game where players roll a ball to collect 12 cubes, with a main menu and scoring system.

**Current Status:** Zero implementation - no scripts, prefabs, materials, or gameplay elements exist. Scene is empty.

**Implementation Phases:**
- **Phase 0:** Foundation (directories, scripts, prefabs, materials) - **MUST DO FIRST**
- **Phase 1:** Core gameplay (scene setup, collectibles, HUD) - **REQUIRED FOR MVP**
- **Phase 2:** Main menu system - **REQUIRED BY SPEC**
- **Phase 3:** Input enhancements (ESC key, mouse controls) - **MEDIUM PRIORITY**
- **Phase 4:** Polish (visual effects, audio, lighting) - **LOW PRIORITY**
- **Phase 5:** Testing and validation - **ONGOING**

**Estimated Tasks:**
- Phase 0: ~45 tasks (foundation)
- Phase 1: ~25 tasks (gameplay)
- Phase 2: ~15 tasks (menu)
- Phase 3: ~15 tasks (input)
- Phase 4: ~30 tasks (polish)
- Phase 5: ~42 tasks (testing)
- **Total: ~172 tasks**

### Analysis Complete ✓
**Status:** Project is at ZERO implementation - NO game scripts, NO prefabs, NO materials, EMPTY scene, NO directories.  
**Spec Location:** `/Assets/BeziBridge/specs/game_spec.md`  
**Analysis Document:** Page: `Documentation/Project Analysis`  
**Implementation Plan:** Page: `IMPLEMENTATION_PLAN` (detailed phase-by-phase plan)  
**Critical Path:** Create Directories → Implement Phase 0 → Phase 1 (Core Gameplay) → Phase 2 (Main Menu) → Achieve Playable Game  
**Last Updated:** Prompt 1 (Initial Analysis Complete) - Comprehensive project analysis performed. Confirmed:
- Scene contains only default URP objects (Main Camera, Directional Light, Global Volume)
- Broken script reference found: `Assembly-CSharp::CameraController` on Main Camera (missing script)
- No `/Assets/Scripts`, `/Assets/Materials`, `/Assets/Prefabs`, `/Assets/Models` directories exist
- No `/Assets/_GAME/Scripts` directory exists
- **ZERO** game-related C# scripts found anywhere in project (searched all assets)
- **ZERO** materials found in project
- **ZERO** prefabs found in project
- InputSystem_Actions.inputactions exists at `/Assets/InputSystem_Actions.inputactions` but contents not verified
- No Main Menu scene exists (only SampleScene.unity in `/Assets/_GAME/Scenes/`)
- No shared utilities or helper scripts found in `/Assets/` directory
- Unity 6000.3 with URP 17.3.0, Input System 1.17.0 installed and ready
- **NEXT STEP:** Begin Phase 0 implementation starting with directory creation

### Phase 0: Project Structure Setup (CRITICAL - REQUIRED FIRST)

- [ ] **Create Directory Structure**
  - [ ] Create `/Assets/Scripts` directory for shared utility scripts
  - [ ] Create `/Assets/Materials` directory for materials
  - [ ] Create `/Assets/Prefabs` directory for prefabs
  - [ ] Create `/Assets/Models` directory for 3D models (optional, future use)
  - [ ] Create `/Assets/_GAME/Scripts` directory for game-specific scripts
  - [ ] Verify directory structure matches project rules

- [ ] **Create Materials**
  - [ ] Create `/Assets/Materials/GroundMaterial.mat` (URP/Lit shader)
  - [ ] Create `/Assets/Materials/WallMaterial.mat` (URP/Lit shader)
  - [ ] Create `/Assets/Materials/PlayerMaterial.mat` (URP/Lit shader)
  - [ ] Create `/Assets/Materials/CollectibleMaterial.mat` (URP/Lit shader with emission)
  - [ ] Create `/Assets/Materials/PlayerPhysics.physicsMaterial` (3D physics material)
  - [ ] Configure physics material: friction ~0.3, bounciness ~0.5

- [ ] **Create Core Scripts** (in `/Assets/_GAME/Scripts/`)
  - [ ] Create `PlayerController.cs` - handles player movement via Input System
  - [ ] Create `Collectible.cs` - handles collection on trigger enter
  - [ ] Create `CameraController.cs` - follows player with offset
  - [ ] Create `GameManager.cs` - manages game state and win condition
  - [ ] Create `UIManager.cs` - manages score display and win panel
  - [ ] Create `CollectibleSpawner.cs` - spawns 12 collectibles in circle

- [ ] **Create Prefabs**
  - [ ] Create Player prefab at `/Assets/Prefabs/Player.prefab`
    - Sphere primitive with scale (1, 1, 1)
    - Add Rigidbody component (mass: 1, drag: 0, angular drag: 0.05)
    - Add SphereCollider component
    - Assign PlayerMaterial to renderer
    - Assign PlayerPhysics to collider
    - Add PlayerController component
    - Add PlayerInput component (assign InputSystem_Actions)
    - Set tag to "Player"
  - [ ] Create Collectible prefab at `/Assets/Prefabs/Collectible.prefab`
    - Cube primitive with scale (0.5, 0.5, 0.5)
    - Add BoxCollider component with isTrigger = true
    - Assign CollectibleMaterial to renderer
    - Add Collectible component
    - Add rotation script or animation (45 deg/sec on Y axis)
    - Set tag to "Collectible"

### Phase 1: Core Gameplay Setup (HIGH PRIORITY - REQUIRED FOR PLAYABLE GAME)

- [ ] **Scene Setup - Game Scene**
  - [ ] Create ground plane GameObject with appropriate scale (20x1x20 recommended)
  - [ ] Add MeshRenderer and MeshCollider to ground
  - [ ] Apply GroundMaterial to ground plane
  - [ ] Create 4 wall GameObjects around perimeter (North, South, East, West)
  - [ ] Add BoxColliders to walls and configure dimensions (height ~2, thickness ~0.5)
  - [ ] Position walls at edges (X: ±10, Z: ±10 for 20x20 ground)
  - [ ] Apply WallMaterial to walls
  - [ ] Instantiate Player prefab at position (0, 0.5, 0)
  - [ ] Verify Player tag is "Player" (should be set in prefab)
  - [ ] Configure Main Camera position (0, 15, -15) and rotation (45, 0, 0) for angled top-down view
  - [ ] Add CameraController component to Main Camera
  - [ ] Assign Player transform to CameraController.player reference in inspector
  - [ ] Set CameraController offset to (0, 10, -10) or adjust as needed

- [ ] **Collectibles System**
  - [ ] Create CollectibleSpawner.cs in /Assets/_GAME/Scripts/
  - [ ] Add serialized field for collectiblePrefab reference (Collectible.prefab)
  - [ ] Add configurable collectibleCount field (default: 12)
  - [ ] Add configurable spawnRadius field (default: 8f)
  - [ ] Implement Start() method to spawn collectibles
  - [ ] Calculate circular spawn positions using trigonometry:
    - angle = i * (360 / count) converted to radians
    - x = Cos(angle) * radius
    - z = Sin(angle) * radius
    - y = 0.5 (to rest on ground)
  - [ ] Instantiate collectibles at calculated positions
  - [ ] Create empty GameObject named "CollectibleSpawner" in scene
  - [ ] Add CollectibleSpawner component
  - [ ] Assign Collectible prefab reference in inspector
  - [ ] Test spawn: verify exactly 12 collectibles in circular pattern
  - [ ] Verify Collectible prefab has BoxCollider with isTrigger = true
  - [ ] Verify Collectible prefab is tagged as "Collectible"

- [ ] **HUD Setup**
  - [ ] Create UI Canvas GameObject (Screen Space - Overlay)
  - [ ] Add CanvasScaler component with proper reference resolution
  - [ ] Create ScoreText GameObject with TextMeshProUGUI component
  - [ ] Position ScoreText at top center (anchor: top center)
  - [ ] Configure ScoreText font size and alignment
  - [ ] Create WinPanel GameObject (child of Canvas)
  - [ ] Add Image component to WinPanel for background
  - [ ] Create victory message Text and Restart button in WinPanel
  - [ ] Add UIManager component to Canvas
  - [ ] Assign scoreText and winPanel references in UIManager
  - [ ] Wire Restart button OnClick to UIManager.RestartGame

- [ ] **GameManager Setup**
  - [ ] Create empty GameObject named "GameManager"
  - [ ] Add GameManager component
  - [ ] Verify it finds UIManager on Start
  - [ ] Test score counting and win condition

### Phase 2: Main Menu System (HIGH PRIORITY - REQUIRED BY SPEC)

- [ ] **Main Menu Scene Creation**
  - [ ] Create new scene: /Assets/_GAME/Scenes/MainMenu.unity
  - [ ] Add UI Canvas (Screen Space - Overlay)
  - [ ] Add CanvasScaler with reference resolution (1920x1080)
  - [ ] Create EventSystem for UI interaction
  - [ ] Add Panel for background (optional, for visual appeal)
  - [ ] Create TitleText (TextMeshProUGUI) - display game title "Roll-A-Ball"
  - [ ] Position TitleText at upper-middle of screen
  - [ ] Create ButtonNewGame (Button - TextMeshProUGUI)
  - [ ] Position NewGame button below title
  - [ ] Create ButtonQuit (Button - TextMeshProUGUI)
  - [ ] Position Quit button below NewGame button
  - [ ] Style buttons with proper colors and font sizes

- [ ] **Main Menu Controller**
  - [ ] Create MainMenuManager.cs in /Assets/_GAME/Scripts/
  - [ ] Implement LoadGameScene method using SceneManager.LoadScene
  - [ ] Implement QuitGame method using Application.Quit
  - [ ] Add #if UNITY_EDITOR wrapper for editor-safe quit behavior
  - [ ] Attach MainMenuManager to Canvas or dedicated GameObject
  - [ ] Wire ButtonNewGame.onClick to LoadGameScene
  - [ ] Wire ButtonQuit.onClick to QuitGame

- [ ] **Scene Management & Build Settings**
  - [ ] Open Build Settings (File → Build Settings)
  - [ ] Add MainMenu.unity as scene index 0
  - [ ] Add SampleScene.unity as scene index 1
  - [ ] Verify scene build order
  - [ ] Test scene loading from MainMenu to SampleScene
  - [ ] Test win screen restart (should reload SampleScene)
  - [ ] Test full flow: Main Menu → New Game → Play → Win → Restart → Menu

### Phase 3: Input & Game Flow Enhancement (MEDIUM PRIORITY)

- [ ] **ESC Key Functionality**
  - [ ] Open InputSystem_Actions.inputactions in Input Actions editor
  - [ ] Add new action "Cancel" or "Quit" in Player action map
  - [ ] Bind ESC key to Cancel action
  - [ ] Add OnCancel(InputValue) method to GameManager or new InputHandler
  - [ ] Implement return to MainMenu when ESC pressed during gameplay
  - [ ] Use SceneManager.LoadScene("MainMenu") or scene index 0
  - [ ] Consider pause menu as alternative (optional)

- [ ] **Mouse Input Investigation**
  - [ ] Review game_spec.md for mouse control requirement clarity
  - [ ] Spec mentions "mouse or keyboard" for rolling
  - [ ] Research: Does "mouse" mean click-drag, position-based, or other?
  - [ ] If required: Determine mouse input scheme with stakeholder
  - [ ] If required: Add Mouse Position action to Input Actions
  - [ ] If required: Implement mouse-to-movement conversion in PlayerController
  - [ ] If not required: Mark as out-of-scope and use WASD only

- [ ] **Player Prefab Configuration**
  - [ ] Open Player prefab in Prefab mode
  - [ ] Verify PlayerInput component exists
  - [ ] Assign InputSystem_Actions asset to PlayerInput.actions
  - [ ] Set Behavior to "Invoke Unity Events" or "Send Messages"
  - [ ] Verify Player tag is assigned
  - [ ] Verify Rigidbody settings (Mass: 1, Drag: ~0, Angular Drag: ~0.05)
  - [ ] Apply PlayerPhysics material to sphere collider
  - [ ] Test input responsiveness in play mode

- [ ] **Game State Management Enhancement**
  - [ ] Add GameState enum to GameManager (Menu, Playing, Paused, Won)
  - [ ] Track current state
  - [ ] Disable player input during Won state
  - [ ] Add state transition logging for debugging
  - [ ] Consider time scale management for pause (optional)

### Phase 4: Visual & Audio Polish (LOW PRIORITY - POST-MVP)

- [ ] **Collectible Visual Feedback**
  - [ ] Create particle system prefab for pickup effect
  - [ ] Add ParticleSystem to Collectible prefab or spawn on collection
  - [ ] Configure emission, shape, color over lifetime
  - [ ] Instantiate particles before Destroy in Collectible.OnTriggerEnter
  - [ ] Add scale tween animation on collection (optional)
  - [ ] Add color flash or pulse effect (optional)

- [ ] **Audio System**
  - [ ] Create /Assets/_GAME/Audio folder for organization
  - [ ] Import or create collectible pickup sound effect (.wav/.mp3)
  - [ ] Add AudioSource component to Collectible prefab
  - [ ] Configure AudioClip and Play on pickup
  - [ ] Import or create background music loop
  - [ ] Add AudioSource to GameManager or Main Camera for BGM
  - [ ] Create UI button click sound
  - [ ] Add AudioSource to buttons with click sound
  - [ ] Create win sound effect
  - [ ] Play win sound when ShowWinScreen is called

- [ ] **Material & Lighting Enhancement**
  - [ ] Review and enhance CollectibleMaterial (add emission, metallic)
  - [ ] Review and enhance PlayerMaterial (brightness, smoothness)
  - [ ] Review and enhance GroundMaterial (tiling, normal map optional)
  - [ ] Adjust Directional Light intensity and color temperature
  - [ ] Add Skybox material (optional)
  - [ ] Configure Global Volume for post-processing
  - [ ] Add Bloom, Tonemapping, Color Grading overrides
  - [ ] Test visual quality on different displays

- [ ] **UI Polish**
  - [ ] Design better button sprites/backgrounds
  - [ ] Add button hover/press animations using Unity UI Animation
  - [ ] Improve font choice and readability
  - [ ] Add consistent color scheme across all UI
  - [ ] Add logo or title graphic (optional)
  - [ ] Design better Win Panel layout with celebratory message
  - [ ] Add UI fade-in/out transitions between scenes (optional)

### Phase 5: Testing & Validation (ONGOING - THROUGHOUT DEVELOPMENT)

- [ ] **Scene Setup Validation**
  - [ ] Verify ground plane has correct collider
  - [ ] Verify walls prevent ball from rolling off edges
  - [ ] Verify player spawns at center (0, 0.5, 0)
  - [ ] Verify camera follows player smoothly
  - [ ] Check no collider gaps or physics glitches

- [ ] **Collectible System Testing**
  - [ ] Verify exactly 12 collectibles spawn
  - [ ] Verify circular pattern is equidistant and centered
  - [ ] Verify collectibles rotate continuously
  - [ ] Test collision detection (ball must touch, not pass through)
  - [ ] Verify collectibles disappear on collection
  - [ ] Check for any remaining collectibles after spawn

- [ ] **Score & Win Condition Testing**
  - [ ] Verify score starts at 0/12
  - [ ] Collect one cube, verify score updates to 1/12
  - [ ] Collect all 12 cubes, verify score shows 12/12
  - [ ] Verify win screen appears automatically at 12/12
  - [ ] Test restart button returns to game with fresh state
  - [ ] Verify score resets to 0/12 on restart

- [ ] **Input Testing**
  - [ ] Test W key moves ball forward (positive Z)
  - [ ] Test S key moves ball backward (negative Z)
  - [ ] Test A key moves ball left (negative X)
  - [ ] Test D key moves ball right (positive X)
  - [ ] Test diagonal movement (WA, WD, SA, SD)
  - [ ] Test input responsiveness and feel
  - [ ] Test ESC key returns to main menu (after Phase 3)
  - [ ] Test no input response during win screen

- [ ] **Main Menu & Scene Flow Testing**
  - [ ] Launch game, verify Main Menu appears first
  - [ ] Click "New Game", verify SampleScene loads
  - [ ] Play game to completion, verify win screen
  - [ ] Click restart, verify scene reloads correctly
  - [ ] Use ESC to return to menu, click New Game again
  - [ ] Click "Quit Game" button, verify application quits
  - [ ] Test in build (standalone), not just editor

- [ ] **Physics & Performance Testing**
  - [ ] Verify ball physics feel good (not too fast/slow)
  - [ ] Check for physics jitter or instability
  - [ ] Verify walls have proper collision response
  - [ ] Test frame rate is smooth (60 FPS target)
  - [ ] Profile with Unity Profiler if performance issues
  - [ ] Check for memory leaks after multiple restarts

- [ ] **UI & Resolution Testing**
  - [ ] Test UI layout at 1920x1080
  - [ ] Test UI layout at 1280x720
  - [ ] Test UI layout at ultrawide resolutions (optional)
  - [ ] Verify text is readable at all resolutions
  - [ ] Verify buttons are clickable and sized appropriately
  - [ ] Check UI anchor settings for responsive design

- [ ] **Edge Case Testing**
  - [ ] Test restarting game multiple times in a row
  - [ ] Test quitting during gameplay
  - [ ] Test scene loading without errors or warnings
  - [ ] Verify no null reference exceptions in console
  - [ ] Test with "Collectible" tag missing (should warn, not crash)
  - [ ] Test with missing UI references (should warn gracefully)

### Notes

**Critical Path to Playable Game:**
1. **Phase 0** (Project Structure) - MUST be completed first, creates all foundation assets
   - Directory structure per project rules
   - All materials (ground, wall, player, collectible, physics)
   - All core scripts (6 total scripts)
   - Both prefabs (Player and Collectible)
2. **Phase 1** (Core Gameplay) - MUST be completed for minimum viable playable game
   - Scene setup with ground, walls, player, camera
   - Collectible spawner system (critical - game cannot function without collectibles)
   - HUD with score display and win screen
   - GameManager integration
3. **Phase 2** (Main Menu) - REQUIRED by specification document
   - Main menu scene and controller
   - Scene management and transitions
   - Build settings configuration
4. **Phase 3** (Input & Flow) - MEDIUM priority enhancements
5. **Phase 4** (Polish) - LOW priority, post-MVP features
6. **Phase 5** (Testing) - ONGOING throughout all phases

**Current Blockers (Critical):**
- **Phase 0 must be completed first** - No directories exist for organizing assets per project rules
- **No materials exist** - Cannot create prefabs without materials
- **No scripts exist** - Cannot add components to prefabs without scripts
- **No prefabs exist** - Cannot instantiate player or collectibles in scene
- SampleScene is completely empty - no ground, walls, player, or collectibles exist
- No UI Canvas or UI elements exist in scene
- No GameManager instance exists in scene
- Main Menu scene does not exist

**Dependency Chain:**
1. Phase 0 (directories + materials + scripts + prefabs) → MUST BE DONE FIRST
2. Phase 1 (scene setup using prefabs and materials from Phase 0)
3. Phase 2 (main menu using scripts from Phase 0)
4. Phases 3-5 (enhancements and testing)

**Architecture Decisions Made:**
- Component-based design with minimal coupling (current pattern)
- GameManager as singleton-like central coordinator (uses FindFirstObjectByType)
- UIManager handles all UI presentation
- CollectibleSpawner will be new script to handle procedural collectible placement
- Input System package for all input (already integrated)
- Scene-based architecture for menu/game separation
- TextMeshPro for all text rendering

**Implementation Order Rationale:**
1. **Phase 0 (Project Structure)** - Foundation layer, nothing can be built without these assets
2. **Scene Setup First** - Cannot test any systems without a playable environment
3. **Collectible Spawner** - Game is unplayable without collectibles to collect
4. **UI Setup** - Needed to display score and win condition
5. **Main Menu** - Required by spec, but game can be tested in editor without it
6. **Polish** - Added after core functionality is proven and working

**Known Technical Debt:**
- Need to verify InputSystem_Actions.inputactions is properly configured (contents unknown)
- May need to create Input Actions asset if current one is invalid
- No shared utility library (not critical, but could centralize common patterns)
- Collectible rotation needs implementation (script or animator component)

**Confirmed Non-Issues:**
- No duplicate physics material files exist yet (will create one properly in Phase 0)

**Specification Clarifications Needed:**
- Mouse control mechanism (spec says "mouse or keyboard" but doesn't specify how mouse works)
  - Is it: position-based, click-drag, or just mention of alternative input?
  - Current implementation only supports WASD keyboard input
  - Recommend clarifying before implementing mouse if required

**Testing Strategy:**
- Test each phase incrementally as implemented
- Validate scene setup before proceeding to collectibles
- Test collectible spawn pattern thoroughly (exact count and positioning)
- Full integration test after Phase 1 completion
- Build and test standalone executable after Phase 2
- Edge case testing throughout Phase 5

**Success Criteria (Minimum Viable Product):**
- ✓ All directories created per project rules
- ✓ All materials and physics materials created
- ✓ All 6 core scripts created and compiled without errors
- ✓ Player and Collectible prefabs created with proper components
- Player can start game from Main Menu
- Player spawns in center of playing field
- 12 collectibles spawn in circular pattern
- Player can roll ball with WASD controls
- Camera follows player smoothly
- Collectibles disappear when touched
- Score increments with each collection (1-12)
- Win screen appears when all 12 collected
- Player can restart game
- Player can quit to Main Menu or exit application
- No errors or warnings in console
- Game runs at stable 60 FPS

**Phases Summary:**
- **Phase 0:** Create all foundation assets (6 scripts, 2 prefabs, 4+ materials, directory structure)
- **Phase 1:** Build playable game scene (ground, walls, player, collectibles, camera, HUD)
- **Phase 2:** Build main menu scene and wire up scene transitions
- **Phase 3:** Add ESC key functionality and enhance input options
- **Phase 4:** Visual and audio polish (particles, sounds, lighting)
- **Phase 5:** Comprehensive testing and validation
