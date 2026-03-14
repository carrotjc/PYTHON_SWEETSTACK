import pygame
 
 
class SoundManager:
    """
    Central sound controller for Sweet Stack.
 
    Sounds are keyed by short names and loaded once on init.
    Call play(name) anywhere in the game — safe to call even
    if the file is missing or mixer failed to initialise.
    """
 
    # Map short name → file path
    _SOUND_PATHS = {
        "start":      "assets/sounds/sfx_start.wav",      # play button pressed
        "click":      "assets/sounds/sfx_click.wav",      # ingredient button selected
        "correct":    "assets/sounds/sfx_correct.wav",    # order submitted correctly
        "wrong":      "assets/sounds/sfx_wrong.wav",      # wrong order / incomplete
        "reset":      "assets/sounds/sfx_reset.wav",      # reset button pressed
        "timer_warn": "assets/sounds/sfx_timer_warn.wav", # plays once when ≤5s left
        "gameover":   "assets/sounds/sfx_gameover.wav",   # round 3 ends
    }
 
    # Volume per sound (0.0 – 1.0)
    _VOLUMES = {
        "start":      0.8,
        "click":      0.6,
        "correct":    0.9,
        "wrong":      0.8,
        "reset":      0.5,
        "timer_warn": 0.7,
        "gameover":   0.9,
    }
 
    def __init__(self):
        self._sounds: dict[str, pygame.mixer.Sound | None] = {}
        self._enabled = pygame.mixer.get_init() is not None
 
        if not self._enabled:
            return
 
        for name, path in self._SOUND_PATHS.items():
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(self._VOLUMES.get(name, 0.7))
                self._sounds[name] = snd
            except FileNotFoundError:
                # Missing file — skip silently
                self._sounds[name] = None
            except pygame.error:
                self._sounds[name] = None
 
    def play(self, name: str):
        """Play a sound by its short name. Safe to call if sound is missing."""
        if not self._enabled:
            return
        snd = self._sounds.get(name)
        if snd:
            snd.play()
 
    def stop(self, name: str):
        """Stop a specific sound if it is currently playing."""
        if not self._enabled:
            return
        snd = self._sounds.get(name)
        if snd:
            snd.stop()