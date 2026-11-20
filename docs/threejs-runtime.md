# Three.js dependency and graceful fallback

This initial math-posts build uses **Three.js r160** via the pinned ESM endpoint `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js`, MIT-licensed (upstream: <https://github.com/mrdoob/three.js/tree/r160>). The current release therefore **does not claim an offline Three.js bundle**. For privacy/performance, 2D articles load no Three.js dependency. Three 3D posts have standalone SVGs rendered by default; JavaScript/WebGL/network errors leave those SVGs visible and the proof remains readable.

Planned upgrade based on user feedback: vendor the audited ESM build, include license, SHA-256 and offline Chromium test. Verify GPU path and touch/keyboard camera separately.
