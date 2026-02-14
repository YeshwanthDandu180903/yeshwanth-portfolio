# Portfolio Animation & Theme Configuration (Save State)
# Date: 2026-02-14
# Preset Name: "Data Science Dark Mode - Sleek"

This file contains the exact configuration for the current "Premium Dark" theme and its animations. Use this as a reference to restore or modify features without losing the current look.

---

## 1. Core Theme & Background
**Goal:** A consistent, high-end dark mode without "blocky" transitions.
- **Body Background:** Static Radial Gradient (No moving colors).
  - Code: `background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #0a0a0a 100%);`
- **Section Backgrounds (.bg-darker):** Transparent overlay to let the body gradient show through.
  - Code: `background-color: rgba(0, 0, 0, 0.4);`
- **Glass Effect:** Used on cards (`.glass-card`).
  - Background: `rgba(255, 255, 255, 0.05)`
  - Border: `1px solid rgba(255, 255, 255, 0.1)`

## 2. Active Animations

### A. AI/Math Particle Background
- **Type:** HTML5 Canvas (`#bg-canvas`).
- **Logic:** Floating text particles.
- **Symbols Used:** `['0', '1', 'Σ', '∫', 'π', 'θ', 'λ', 'σ', '{ }', '[]', '</>', 'x', 'y', 'z', 'μ', '∂']`
- **Behavior:** Particles float randomly. Lines connect when `distance < 100px`.
- **Color:** Accent Color (`#00f2c3`) with low opacity.

### B. Code Snippet Typing (Hero Section)
- **Element:** `.code-window` > `#code-typewriter`
- **Effect:** Simulates typing Python code for a Neural Network.
- **Content:**
  ```python
  def train_model(data):
      # Initialize AI
      model = Sequential([...])
      model.fit(data)
  ```
- **Animation Logic:** Lines are revealed one by one (`innerHTML` update) with a blinking cursor at the end.

### C. Live Status Pulse
- **Element:** `.status-badge` > `.pulse-dot`
- **Location:** Hero Section (above profile).
- **CSS Animation:** `pulse-green` (Scale 0.95 -> 1 -> 0.95, Shadow expansion).
- **Purpose:** Signals "Available for Opportunities".

### D. Stats Counter (About Section)
- **Element:** `#stats-counter-section`
- **Trigger:** `IntersectionObserver` (when scrolled into view).
- **Logic:** Counts up from 0 to `data-count` (e.g., 15, 12, 180) over 2 seconds.
- **Style:** Large bold text (`display-5`) with accent gradient.

### E. Graph Drawing Animation
- **Location:** Data Science Skill Card.
- **Element:** `.graph-container` with 5 `.graph-bar` divs.
- **CSS Animation:** `growBar` (Height 0 -> Target Height).
- **Stagger:** Bars have increasing `animation-delay` (0.2s, 0.4s, etc.) to look like a chart loading.

### F. Animated Skill Bars
- **Location:** Skills Section.
- **Element:** `.progress-bar-animated`.
- **Trigger:** `IntersectionObserver`.
- **Logic:** Width expands from 0% to `data-width` (e.g., 90%) when visible.

### G. Magnetic Cursor & Buttons
- **Target:** `.btn`, `.social-icon`, `.nav-link`.
- **Logic:** JS tracks `mousemove` inside button.
- **Effect:** Button translates slightly towards the cursor (`x * 0.3`, `y * 0.5`).
- **Feel:** "Sticky" or "Magnetic".

### H. Main Description Typewriter
- **Element:** `.typing-text` (Hero Section).
- **Text:** "a Problem Solver", "a Data Analyst", "an Aspiring Data Scientist", "Aspiring for GenAI roles".
- **Logic:** Types and deletes characters cyclically.

### I. Navbar Scroll Effect
- **Trigger:** Scroll > 50px.
- **Effect:** Adds `.navbar-scrolled` class.
- **Style:** Background becomes opaque/glassy with shadow.

### J. Section Element Fade-In
- **Target:** `.skill-card`, `.timeline-item`, `.project-card`, `.stat-box`.
- **Trigger:** `IntersectionObserver` (20% visible).
- **Effect:** Adds `.animate-active` class (Opacity 0->1, TranslateY 20px->0).

---

## 3. Restoration Instructions for AI
If you need to restore this theme, verify the following files have these key blocks:

1.  **`css/style.css`**:
    - Check `body` has the `radial-gradient`.
    - Check `.status-badge`, `.code-window`, `.graph-container` styles are present.
    - Check `@keyframes pulse-green`, `@keyframes growBar`.

2.  **`js/main.js`**:
    - Ensure `initParticles()` uses the Symbol list.
    - Ensure `typeCodeSnippet()`, `initStatsObserver()`, `initSkillsObserver()`, `initMagneticCursor()` are defined and called in `DOMContentLoaded`.

3.  **`index.html`**:
    - Check specific HTML structures for `<div class="code-window">`, `<div id="stats-counter-section">`, and `<div class="graph-container">`.

---
**Prompt to Restore:**
> "Restore the 'Data Science Dark Mode' preset. I want the static radial background, the math particles, the Python typing effect in the hero, the magnetic buttons, and the graph animations in the skills card. Use the configuration from `animation_config.md`."
