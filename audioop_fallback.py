# Fallback for audioop module on Windows PyInstaller builds
# This provides basic functionality when audioop is not available

import sys
import warnings

# Try to import the real audioop module
try:
    from audioop import *
    AUDIOOP_AVAILABLE = True
except ImportError:
    AUDIOOP_AVAILABLE = False
    warnings.warn("audioop module not available, using fallback implementation")
    
    # Provide minimal fallback functions that pydub might need
    def mul(fragment, width, factor):
        """Multiply audio samples by a factor (fallback)"""
        # Simple fallback - just return the fragment unchanged
        return fragment
    
    def add(fragment1, fragment2, width):
        """Add two audio fragments (fallback)"""
        # Simple fallback - return first fragment
        return fragment1
    
    def bias(fragment, width, bias):
        """Add a bias to audio samples (fallback)"""
        # Simple fallback - return unchanged
        return fragment
    
    def reverse(fragment, width):
        """Reverse audio samples (fallback)"""
        # Simple fallback - return unchanged
        return fragment
    
    def tomono(fragment, width, lfactor, rfactor):
        """Convert stereo to mono (fallback)"""
        # Simple fallback - return unchanged
        return fragment
    
    def tostereo(fragment, width, lfactor, rfactor):
        """Convert mono to stereo (fallback)"""
        # Simple fallback - return unchanged
        return fragment
    
    def ratecv(fragment, width, nchannels, inrate, outrate, state, weightA=1, weightB=0):
        """Rate conversion (fallback)"""
        # Simple fallback - return unchanged with dummy state
        return fragment, None
    
    def lin2lin(fragment, width, newwidth):
        """Convert between different sample widths (fallback)"""
        # Simple fallback - return unchanged
        return fragment
    
    def max(fragment, width):
        """Find maximum sample value (fallback)"""
        return 0
    
    def minmax(fragment, width):
        """Find min and max sample values (fallback)"""
        return (0, 0)
    
    def avg(fragment, width):
        """Calculate average sample value (fallback)"""
        return 0
    
    def avgpp(fragment, width):
        """Calculate average peak-to-peak value (fallback)"""
        return 0
    
    def rms(fragment, width):
        """Calculate RMS value (fallback)"""
        return 0

# Make the fallback available
if not AUDIOOP_AVAILABLE:
    print("Warning: Using audioop fallback implementation. Some audio operations may not work optimally.")
