from .server import mcp

@mcp.prompt()
def godprofile_aesthetic_guide() -> str:
    """The strict aesthetic rules for generating GodProfile assets. Agents MUST read this before rendering."""
    return """
    GODPROFILE DESIGN SYSTEM - STRICT DIRECTIVES
    --------------------------------------------
    When autonomously generating or refactoring assets for the GodProfile toolkit, adhere to these unyielding rules:
    
    1. NEVER use generic white (#ffffff) or block black (#000000) unless explicitly operating within the `minimalist` or `terminal-hacker` theme engines.
    2. When using `luxury-glass` (The flagship theme):
       - ALWAYS enforce a 12px rounded bounding rectangle (`rx="12"`).
       - ALWAYS overlay a secondary `<rect>` rendering an opacity `0.2` repeating 14x14 grid pattern (`stroke="#1b222c"`).
       - Title fonts should be a sleek sans-serif. Data and tag fonts should be uppercase monospace with heavy letter-spacing (`2px`).
    3. Data Maps (Neural Networks):
       - DO NOT render linear point-to-point crosshatching.
       - Use mathematically positioned smooth Cubic Bezier paths (`<path d="M x1 y1 C cx cy, cx cy, x2 y2" />`) to avoid text overlap.
       - Include hidden tracking `<circle>` elements with overlapping `<animateMotion>` directives along the paths to simulate active streaming.
    4. Workflow Injection:
       - Always default to midnight cron timings (`0 0 * * *`) when registering automated stats scripts in `.github/workflows/`.
    """
