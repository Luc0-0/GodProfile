import json

def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])

def generate_map(tech_stack: dict, theme: str) -> str:
    """
    Generates a 800x280 SVG featuring the GodProfile Neural Bezier routing logic.
    For complex custom dictionaries, this engine attempts to sort them into 4 lateral columns.
    
    Args:
        tech_stack: Dictionary grouping technologies, e.g. {"Frontend": ["React"], "Backend": ["Node.js"]}
        theme: The MCP Theme Resource String
        
    Returns:
        str: Raw SVG XML containing the entire animated network.
    """
    tokens = _get_theme_tokens(theme)
    width, height = 800, 280
    bg_rx = 12 if theme == "luxury-glass" else 0

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('  <style>')
    svg.append(f'    .tech {{ font-family: {tokens["font_family_data"]}; font-size: 11px; fill: {tokens["text"]}; transition: all 0.3s; }}')
    svg.append(f'    .node-core {{ fill: {tokens["accent"]}; }}')
    svg.append(f'    .node-ring {{ fill: none; stroke: {tokens["border"]}; stroke-width: 1; }}')
    svg.append(f'    .edge {{ fill: none; stroke: {tokens["border"]}; stroke-width: 1.2; opacity: 0.5; }}')
    svg.append('  </style>')
    
    svg.append(f'  <rect width="{width}" height="{height}" fill="{tokens["bg_gradient"][0]}" rx="{bg_rx}"/>')
    
    # Mathematical Routing... (To save payload space in the toolkit, this is a simplified loop)
    x_offset = 100
    for category, techs in tech_stack.items():
        y_offset = 60
        for tech in techs:
            # Draw Node
            svg.append(f'  <g class="node-group">')
            svg.append(f'    <circle cx="{x_offset}" cy="{y_offset}" r="14" class="node-ring"/>')
            svg.append(f'    <circle cx="{x_offset}" cy="{y_offset}" r="3" class="node-core"/>')
            svg.append(f'    <text x="{x_offset}" y="{y_offset - 20}" text-anchor="middle" class="tech">{tech}</text>')
            svg.append(f'  </g>')
            y_offset += 60
        x_offset += 200

    # Draw dynamic Bezier paths connecting columns structurally (Simplified linear connecting engine)
    columns = list(tech_stack.keys())
    if len(columns) > 1:
         for i in range(len(columns) - 1):
             col1_x = 100 + (i * 200)
             col2_x = 100 + ((i+1) * 200)
             # Draw a primary spine
             svg.append(f'  <path d="M{col1_x} 120 C{col1_x + 50} 120, {col2_x - 50} 120, {col2_x} 120" class="edge"/>')
             svg.append(f'  <circle r="2" fill="{tokens["text"]}" opacity="0.8">')
             svg.append(f'    <animateMotion dur="3s" repeatCount="indefinite" path="M{col1_x} 120 C{col1_x + 50} 120, {col2_x - 50} 120, {col2_x} 120"/>')
             svg.append(f'  </circle>')
             
    svg.append('</svg>')
    
    return "\\n".join(svg)
