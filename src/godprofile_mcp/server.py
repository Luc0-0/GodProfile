import asyncio
import os
import sys

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Ensure the core is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# We will implement these modules sequentially.
try:
    from core import (
        bento_layout, svg_rendering, neural_bezier_engine, github_ci_automation,
        spotify_now_playing, wakatime_metrics, snake_game_injector,
        isometric_3d_globe, blog_fetcher, terminal_emulator, icon_marquee,
        animated_banner, github_trophies
    )
except ImportError:
    pass

# Initialize the MCP Server
mcp = FastMCP("GodProfile")

@mcp.tool()
def refactor_readme_to_bento(readme_content: str) -> str:
    """
    Parses a user's standard GitHub Markdown and restructures it into modern, 
    """
    return bento_layout.generate_bento_matrix(
        readme_content.split("\\n")[0], # dummy payload handling
        readme_content.split("\\n")[1:]
    )

@mcp.tool()
def render_svg_widget(theme: str, data: dict, output_path: str) -> str:
    """
    Generates extremely high-fidelity glassmorphic SVG cards with 12px borders 
    """
    return svg_rendering.generate_svg_card(
        theme=theme,
        title=data.get("title", "Project"),
        description=data.get("description", "Description"),
        tags=data.get("tags", []),
        identifier=data.get("identifier", "RAW")
    )

@mcp.tool()
def generate_neural_network_map(tech_stack: dict, theme: str, output_path: str) -> str:
    """
    Overhauls simple tech stack lists into visually stunning, data-connected 
    """
    return neural_bezier_engine.generate_map(tech_stack, theme)

@mcp.tool()
def setup_github_automation(features: list, repo_path: str) -> str:
    """
    Generates Python scraper scripts and .github/workflows YAMLs to automate 
    stat synchronization (stars, commits, tracking) into the custom SVGs smoothly.
    """
    return github_ci_automation.generate_ci_workflow(features, repo_path)

@mcp.tool()
def render_spotify_now_playing() -> str:
    """Generates dynamic SVGs mimicking the Spotify UI synced to live playback."""
    return spotify_now_playing.setup_spotify_cron("repo", "id", "secret")

@mcp.tool()
def render_wakatime_activity_chart(theme: str) -> str:
    """Constructs perfectly themed pie charts mapping coding language telemetry."""
    return wakatime_metrics.render_wakatime_activity_chart(theme, {})

@mcp.tool()
def setup_contribution_snake(theme: str) -> str:
    """Configures the SVGs of a snake eating the user's contribution grid, re-themed."""
    return snake_game_injector.setup_contribution_snake(theme, "repo")

@mcp.tool()
def render_3d_contribution_globe() -> str:
    """Injects CSS/JS or isometric SVGs rendering the GitHub globe."""
    return isometric_3d_globe.generate_globe()

@mcp.tool()
def fetch_latest_blog_posts(provider: str, username: str, theme: str) -> str:
    """Fetches Dev.to/Medium articles and formats them into the Bento grid."""
    return blog_fetcher.fetch_articles(provider, username, theme)

@mcp.tool()
def render_terminal_emulator_svg(commands: list, theme: str) -> str:
    """Generates Neofetch-style text outputs for Hacker themes."""
    return terminal_emulator.create_typing_svg(commands, theme)

@mcp.tool()
def generate_animated_icon_marquee(icons: list, theme: str) -> str:
    """Creates CSS-driven infinitely scrolling horizontal bands of technology logos."""
    return icon_marquee.build_marquee(icons, theme)

@mcp.tool()
def capture_animated_banner_gif(theme: str, lines: list, path: str) -> str:
    """Invokes Playwright to render complex HTML terminal typing animations into looping GIFs."""
    return animated_banner.capture_banner_gif(theme, lines, path)

@mcp.tool()
def render_github_trophies(username: str, theme: str) -> str:
    """Aesthetically overhauls GitHub trophies into custom SVGs."""
    return github_trophies.generate_trophy_case(username, theme)

def main():
    """Main entrypoint hook for the pyproject.toml package."""
    # Ensure modules containing decorators are loaded so they register on the `mcp` instance
    from . import resources
    from . import prompts
    
    mcp.run()

if __name__ == "__main__":
    main()
