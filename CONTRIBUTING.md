# Contributing to GodProfile

Welcome to the GodProfile MCP Server! Thank you for wanting to make GitHub profiles infinitely more aesthetic and powerful.

## 🛠 Adding a New MCP Tool

Because GodProfile is an MCP (Model Context Protocol) Server, adding new functionality is incredibly straightforward. You do not need to build complex wrappers.

1. **Create your Core Logic**: Write a new python module inside `src/godprofile_mcp/core/`.
2. **Expose the Endpoint**: Import your module into `src/godprofile_mcp/server.py` and wrap it in the FastMCP decorator:
   ```python
   @mcp.tool()
   def render_new_widget(theme: str) -> str:
       """Description of what your tool does. Claude reads this!"""
       return my_core_module.generate()
   ```

## 🎨 Adding a New Theme Resource

Themes dictate the visual rules for the tools (colors, fonts, radii). To add a new one:
1. Open `src/godprofile_mcp/resources.py`.
2. Append your theme dictionary to the `THEMES` object. Ensure it provides standard tokens like `bg_gradient`, `accent`, `border`, and typography strings.

## Rules
- Keep tools fully deterministic.
- Do not utilize third-party SaaS stat counters directly in SVGs (like vercel endpoints) unless requested. Generate the SVG mathematically within Python.
- Always include type hints.
