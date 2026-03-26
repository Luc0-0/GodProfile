def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


def create_typing_svg(commands: list, theme: str) -> str:
    """
    Creates a 600x340 SVG terminal window with typewriter animation.

    Args:
        commands: list of strings e.g. ["$ whoami", "nipun", "$ uname -a", "Linux..."]
        theme: theme name string

    Returns:
        SVG string
    """
    tokens = _get_theme_tokens(theme)
    accent = tokens.get("accent", "#00ff41")
    text_color = tokens.get("text", "#c9d1d9")
    font = tokens.get("font_family_data", "monospace")

    # Layout constants
    width = 600
    height = 340
    line_height = 22
    font_size = 14
    pad_x = 20
    pad_y = 60  # below chrome bar

    # Build CSS keyframes: each line fades in at staggered delays
    # Each line gets a unique animation that goes from opacity 0 to 1
    delay_per_line = 0.8  # seconds between each line appearing

    css_rules = []
    for i in range(len(commands)):
        delay = i * delay_per_line
        css_rules.append(
            f".line{i} {{ opacity: 0; animation: reveal 0.1s {delay:.2f}s forwards; }}"
        )

    css_keyframes = "@keyframes reveal { from { opacity: 0; } to { opacity: 1; } }"
    cursor_delay = len(commands) * delay_per_line
    css_cursor = (
        f".cursor {{ opacity: 0; animation: reveal 0.1s {cursor_delay:.2f}s forwards, "
        f"blink 1s {cursor_delay:.2f}s step-end infinite; }}"
    )
    css_blink = "@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }"

    css = "\n    ".join(css_rules)
    full_css = f"""
    {css_keyframes}
    {css_blink}
    {css}
    {css_cursor}
    .terminal-bg {{ font-family: {font}, 'Courier New', monospace; font-size: {font_size}px; }}
    """

    # Build text elements
    text_elements = []
    for i, line in enumerate(commands):
        y = pad_y + i * line_height
        # Determine color: command lines start with $ or #, else output
        is_command = line.lstrip().startswith(("$", "#", ">"))
        color = accent if is_command else text_color
        # Escape XML special chars
        safe_line = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
        )
        text_elements.append(
            f'  <text x="{pad_x}" y="{y}" fill="{color}" class="line{i}">{safe_line}</text>'
        )

    # Cursor position: after last line
    cursor_y = pad_y + len(commands) * line_height
    cursor_element = (
        f'  <rect x="{pad_x}" y="{cursor_y - font_size}" '
        f'width="8" height="{font_size + 2}" fill="{accent}" class="cursor"/>'
    )

    text_block = "\n".join(text_elements)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <style>
    {full_css}
    </style>
    <clipPath id="terminal-clip">
      <rect width="{width}" height="{height}" rx="12" ry="12"/>
    </clipPath>
  </defs>

  <!-- Terminal background -->
  <rect width="{width}" height="{height}" rx="12" ry="12" fill="#1e1e2e"/>

  <!-- Chrome bar -->
  <rect width="{width}" height="36" rx="12" ry="12" fill="#2a2a3e"/>
  <rect y="24" width="{width}" height="12" fill="#2a2a3e"/>

  <!-- Window control circles -->
  <circle cx="20" cy="18" r="6" fill="#ff5f57"/>
  <circle cx="40" cy="18" r="6" fill="#febc2e"/>
  <circle cx="60" cy="18" r="6" fill="#28c840"/>

  <!-- Terminal title -->
  <text x="{width // 2}" y="23" text-anchor="middle" fill="#888" font-size="12"
        font-family="{font}, monospace">terminal</text>

  <!-- Terminal content group -->
  <g class="terminal-bg" clip-path="url(#terminal-clip)">
{text_block}
{cursor_element}
  </g>
</svg>'''

    return svg
