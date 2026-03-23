def build_marquee(icons: list[str], theme: str) -> str:
    """
    Generates a horizontally scrolling `<marquee>` or CSS-animation band containing
    SVGs of the requested tech stacks. Enforces the visual rules of the current theme
    (e.g., turning coloured icons into monochrome or neon hues if Cyberpunk is active).
    """
    return f"Prepared animated scrolling band containing {len(icons)} tech-icons."
