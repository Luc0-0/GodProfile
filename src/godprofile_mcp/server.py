import os
import sys

from mcp.server.fastmcp import FastMCP

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

@mcp.tool()
def fetch_github_trophies_live(username: str, theme: str = "luxury-glass", github_token: str = "") -> str:
    """
    Fetches LIVE GitHub stats (stars, commits, PRs, issues, repos, followers) via the GitHub API,
    then renders an SVG trophy case. Uses stdlib urllib only — no external dependencies.
    github_token: optional personal access token for higher rate limits and private commit counts.
    Falls back to public API without a token (60 req/hr limit).
    """
    import json
    import urllib.request

    def gh(url: str, *, accept: str = "application/vnd.github+json",
           method: str = "GET", body: bytes | None = None) -> dict:
        req = urllib.request.Request(url, method=method, data=body)
        req.add_header("Accept", accept)
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if github_token:
            req.add_header("Authorization", f"Bearer {github_token}")
        if body:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())

    try:
        user = gh(f"https://api.github.com/users/{username}")
        repos = gh(f"https://api.github.com/users/{username}/repos?per_page=100&type=owner")
        pr_r = gh(f"https://api.github.com/search/issues?q=author:{username}+type:pr&per_page=1")
        is_r = gh(f"https://api.github.com/search/issues?q=author:{username}+type:issue&per_page=1")

        commits = 0
        if github_token:
            gql = json.dumps({"query": (
                '{ user(login: "%s") { contributionsCollection {'
                ' totalCommitContributions restrictedContributionsCount } } }'
            ) % username}).encode()
            try:
                resp = gh("https://api.github.com/graphql", method="POST", body=gql)
                cc = resp["data"]["user"]["contributionsCollection"]
                commits = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
            except Exception:
                pass
        else:
            try:
                r = gh(
                    f"https://api.github.com/search/commits?q=author:{username}&per_page=1",
                    accept="application/vnd.github.cloak-preview+json",
                )
                commits = r.get("total_count", 0)
            except Exception:
                pass

        stats = {
            "stars":     sum(r.get("stargazers_count", 0) for r in repos),
            "commits":   commits,
            "prs":       pr_r.get("total_count", 0),
            "issues":    is_r.get("total_count", 0),
            "repos":     user.get("public_repos", 0),
            "followers": user.get("followers", 0),
        }
    except Exception as e:
        return f"<!-- GitHub API error: {e} -->"

    return github_trophies.generate_trophy_case(username, theme, stats)

@mcp.tool()
def fetch_wakatime_chart_live(api_key: str, theme: str = "luxury-glass") -> str:
    """
    Fetches LIVE coding stats from the WakaTime API (last 7 days) and renders a themed SVG bar chart.
    api_key: your WakaTime v1 API key (found at wakatime.com/settings/account).
    Returns a 400xN SVG showing language percentages with animated bars. No external deps.
    """
    return wakatime_metrics.fetch_wakatime_stats(api_key, theme)

@mcp.tool()
def fetch_spotify_now_playing_live(access_token: str, theme: str = "luxury-glass") -> str:
    """
    Fetches the currently playing (or recently played) track from the Spotify API and renders a themed SVG card.
    access_token: a valid Spotify OAuth access token with user-read-currently-playing scope.
    Returns a 400x100 SVG card with track name, artist, and animated equalizer bars.
    """
    return spotify_now_playing.fetch_now_playing(access_token, theme)

def main():
    """Main entrypoint hook for the pyproject.toml package."""
    # These imports trigger decorator registration on the `mcp` instance — required at startup
    from . import (
        prompts,  # noqa: F401
        resources,  # noqa: F401
    )

    mcp.run()

if __name__ == "__main__":
    main()
