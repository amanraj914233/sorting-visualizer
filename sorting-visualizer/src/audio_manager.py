import pygame
import os
import threading
import time

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.initialized = False
        self.setup_audio()
        
    def setup_audio(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.initialized = True
            self.load_sounds()
            print("Audio system initialized successfully")
        except Exception as e:
            print(f"Audio initialization failed: {e}. Running without sound.")
            self.initialized = False
            self.enabled = False
    
    def load_sounds(self):
        """Generate or load sound effects"""
        try:
            # Generate simple beep sounds programmatically
            self.sounds = {
                'swap': self.generate_beep(800, 0.1),
                'compare': self.generate_beep(400, 0.05),
                'select': self.generate_beep(600, 0.08),
                'complete': self.generate_success_sound(),
                'pivot': self.generate_beep(1000, 0.15),
                'merge': self.generate_beep(300, 0.2)
            }
        except Exception as e:
            print(f"Sound generation failed: {e}")
    
    def generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        try:
            import numpy as np
            
            sample_rate = 22050
            n_samples = int(sample_rate * duration)
            
            # Create a sine wave
            t = np.linspace(0, duration, n_samples, False)
            wave = 0.5 * np.sin(2 * np.pi * frequency * t)
            
            # Apply fade in/out to avoid clicks
            fade_samples = int(sample_rate * 0.01)  # 10ms fade
            if fade_samples * 2 < n_samples:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                wave[:fade_samples] *= fade_in
                wave[-fade_samples:] *= fade_out
            
            # Convert to 16-bit format
            wave = (wave * 32767).astype(np.int16)
            
            # Create stereo sound
            stereo_wave = np.column_stack((wave, wave))
            
            # Create pygame sound
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"Beep generation failed: {e}")
            return None
    
    def generate_success_sound(self):
        """Generate a success sound"""
        try:
            import numpy as np
            
            sample_rate = 22050
            duration = 0.5
            n_samples = int(sample_rate * duration)
            
            t = np.linspace(0, duration, n_samples, False)
            
            # Create a rising sequence of notes
            frequencies = [523.25, 659.25, 783.99]  # C, E, G
            wave = np.zeros(n_samples)
            
            segment_length = n_samples // len(frequencies)
            for i, freq in enumerate(frequencies):
                start = i * segment_length
                end = start + segment_length
                if end > n_samples:
                    end = n_samples
                segment_t = t[start:end] - t[start]
                wave[start:end] = 0.3 * np.sin(2 * np.pi * freq * segment_t)
            
            # Apply fade out
            fade_samples = int(sample_rate * 0.1)
            if fade_samples < n_samples:
                fade_out = np.linspace(1, 0, fade_samples)
                wave[-fade_samples:] *= fade_out
            
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"Success sound generation failed: {e}")
            return None
    
    def play_sound(self, sound_type):
        """Play a sound effect in a separate thread"""
        if not self.enabled or not self.initialized:
            return
            
        def play():
            try:
                if sound_type in self.sounds and self.sounds[sound_type]:
                    self.sounds[sound_type].play()
            except Exception as e:
                print(f"Error playing sound {sound_type}: {e}")
        
        # Play sound in separate thread to avoid blocking
        thread = threading.Thread(target=play, daemon=True)
        thread.start()
    
    def toggle_sound(self, enabled=None):
        """Enable or disable sound effects"""
        if enabled is None:
            self.enabled = not self.enabled
        else:
            self.enabled = enabled and self.initialized
        
        return self.enabled
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.initialized:
            pygame.mixer.quit()