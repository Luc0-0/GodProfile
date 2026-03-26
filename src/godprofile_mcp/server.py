import os
import sys

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Ensure the core is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# We will implement these modules sequentially.
try:
    from core import (
        animated_banner,
        bento_layout,
        blog_fetcher,
        github_ci_automation,
        github_trophies,
        icon_marquee,
        isometric_3d_globe,
        neural_bezier_engine,
        snake_game_injector,
        spotify_now_playing,
        svg_rendering,
        terminal_emulator,
        wakatime_metrics,
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
def render_svg_widget(theme: str, data: dict) -> str:
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
def generate_neural_network_map(tech_stack: dict, theme: str) -> str:
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
def render_spotify_now_playing(track: str = "", artist: str = "", theme: str = "luxury-glass", is_playing: bool = True) -> str:
    """
    Generates a 400x100 SVG 'Now Playing' card mimicking the Spotify UI.
    Includes animated equalizer bars when is_playing=True, themed colors, and album art placeholder.
    Also returns a GitHub Actions cron workflow YAML for live Spotify sync if credentials are provided.
    """
    return spotify_now_playing.render_now_playing(track=track, artist=artist, theme=theme, is_playing=is_playing)

@mcp.tool()
def render_wakatime_activity_chart(theme: str, data: dict = {}) -> str:
    """
    Renders a 400x220 SVG horizontal bar chart of coding language activity.
    data: dict mapping language names to percentage floats, e.g. {"Python": 48.3, "TypeScript": 27.1}.
    Uses placeholder data if data is empty. Themed via theme tokens.
    """
    return wakatime_metrics.render_wakatime_activity_chart(theme, data)

@mcp.tool()
def setup_contribution_snake(theme: str) -> str:
    """
    Generates a GitHub Actions workflow YAML that runs Platane/snk to animate the contribution grid
    as a snake game. Injects custom theme hex colors into the workflow environment.
    """
    return snake_game_injector.setup_contribution_snake(theme, "repo")

@mcp.tool()
def render_3d_contribution_globe(theme: str = "luxury-glass", highlight_points: list = []) -> str:
    """
    Generates a 400x400 SVG isometric 3D globe using real spherical-to-isometric projection math.
    Renders 12 longitude + 8 latitude grid lines. Optional highlight_points: list of [lat, lon] pairs.
    Includes slow animated rotation via SVG animateTransform.
    """
    return isometric_3d_globe.generate_globe(theme=theme, highlight_points=highlight_points or None)

@mcp.tool()
def fetch_latest_blog_posts(provider: str, username: str, theme: str) -> str:
    """
    Fetches the latest blog posts from Dev.to, Medium, Hashnode, or any RSS/Atom URL.
    provider: 'devto', 'medium', 'hashnode', or a direct RSS URL.
    Returns a themed SVG card (400x280) displaying up to 5 recent post titles and dates.
    Uses stdlib urllib only — no external dependencies.
    """
    return blog_fetcher.fetch_articles(provider, username, theme)

@mcp.tool()
def render_terminal_emulator_svg(commands: list, theme: str) -> str:
    """
    Generates a 600x340 SVG animated terminal window with macOS-style window chrome.
    commands: alternating list of shell commands and their outputs, e.g. ['$ whoami', 'nipun'].
    Each line animates in sequentially via CSS @keyframes. Blinking cursor at end.
    """
    return terminal_emulator.create_typing_svg(commands, theme)

@mcp.tool()
def generate_animated_icon_marquee(icons: list, theme: str, speed: int = 30) -> str:
    """
    Creates a pure SVG infinitely scrolling horizontal band of technology name badges.
    icons: list of tech names e.g. ['Python', 'React', 'Docker']. speed: animation duration in seconds.
    Uses CSS @keyframes with duplicated rows for seamless infinite loop. No external deps.
    """
    return icon_marquee.build_marquee(icons, theme, speed)

@mcp.tool()
def capture_animated_banner_gif(theme: str, lines: list, path: str = "") -> str:
    """
    Generates a pure SVG animated banner (800x200) with gradient background and sequential text fade-in.
    lines: list of text lines to display. No Playwright required — entirely stdlib SVG generation.
    If path is provided, also saves the SVG to that file path.
    """
    return animated_banner.capture_banner_gif(theme, lines, path)

@mcp.tool()
def render_github_trophies(username: str, theme: str, stats: dict = {}) -> str:
    """
    Generates an 800x200 SVG trophy case with up to 6 trophies (Stars, Commits, PRs, Issues, Repos, Followers).
    stats: dict with integer values e.g. {'stars': 150, 'commits': 1200, 'prs': 45}.
    Trophies are ranked S/A/B/C (gold/silver/bronze/default). S-rank trophies have animated glow.
    """
    return github_trophies.generate_trophy_case(username, theme, stats or None)

def main():
    """Main entrypoint hook for the pyproject.toml package."""
    # Ensure modules containing decorators are loaded so they register on the `mcp` instance
    from . import prompts, resources
    
    mcp.run()

if __name__ == "__main__":
    main()
