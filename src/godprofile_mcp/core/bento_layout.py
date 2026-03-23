def generate_bento_matrix(hero_image: str, widget_images: list[str]) -> str:
    """
    Generates an asymmetric HTML <table> structure matching the GodProfile luxury aesthetic.
    The first image is treated as a Hero span (colspan=2), the subsequent images are placed 
    in a two-column grid.
    
    Args:
        hero_image (str): Markdown or HTML string for the primary image. (e.g. `<img src="...">`)
        widget_images (list[str]): List of HTML strings for the smaller widget images.
        
    Returns:
        str: Raw HTML for the structurally sound Bento box.
    """
    bento_html = [
        '<table align="center" style="border-spacing: 12px; border-collapse: separate;">',
        '  <tr>',
        f'    <td colspan="2" align="center">{hero_image}</td>',
        '  </tr>'
    ]
    
    # Process pairs for the remaining widgets
    for i in range(0, len(widget_images), 2):
        bento_html.append('  <tr>')
        bento_html.append(f'    <td align="center" width="50%">{widget_images[i]}</td>')
        if i + 1 < len(widget_images):
            bento_html.append(f'    <td align="center" width="50%">{widget_images[i+1]}</td>')
        else:
            # Empty column if odd number
            bento_html.append('    <td align="center" width="50%"></td>')
        bento_html.append('  </tr>')
        
    bento_html.append('</table>')
    
    return "\n".join(bento_html)
