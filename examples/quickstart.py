"""
GodProfile MCP Toolkit — Quickstart Demo
Run: python examples/quickstart.py
Outputs SVG files to examples/output/
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from godprofile_mcp.core import (
    bento_layout,
    neural_bezier_engine,
    terminal_emulator,
    icon_marquee,
    animated_banner,
    github_trophies,
    wakatime_metrics,
    spotify_now_playing,
    blog_fetcher,
    isometric_3d_globe,
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save(filename: str, content: str) -> None:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {filename}")


def main():
    theme = "luxury-glass"
    print(f"\nGodProfile Quickstart — theme: {theme}\n")

    print("Generating terminal SVG...")
    svg = terminal_emulator.create_typing_svg(
        commands=["$ whoami", "godmode_user", "$ uname -s", "Linux", "$ echo 'Hello, world!'", "Hello, world!"],
        theme=theme,
    )
    save("terminal.svg", svg)

    print("Generating icon marquee...")
    svg = icon_marquee.build_marquee(
        icons=["Python", "TypeScript", "Rust", "Go", "Docker", "Kubernetes", "React", "FastAPI", "PostgreSQL", "Redis"],
        theme=theme,
    )
    save("icon_marquee.svg", svg)

    print("Generating animated banner...")
    svg = animated_banner.generate_banner(
        title="GodProfile",
        subtitle="MCP Toolkit — forge god-tier GitHub profiles",
        theme=theme,
    )
    save("banner.svg", svg)

    print("Generating GitHub trophies...")
    svg = github_trophies.generate_trophy_case(
        username="nipunnirwana",
        theme=theme,
        stats={"stars": 340, "commits": 2100, "prs": 87, "issues": 54, "repos": 42, "followers": 310},
    )
    save("trophies.svg", svg)

    print("Generating WakaTime chart...")
    svg = wakatime_metrics.render_wakatime_activity_chart(
        theme=theme,
        data={"Python": 48.3, "TypeScript": 27.1, "Rust": 14.2, "Shell": 6.8, "Other": 3.6},
    )
    save("wakatime.svg", svg)

    print("Generating Spotify card...")
    svg = spotify_now_playing.render_now_playing(
        track="Blinding Lights",
        artist="The Weeknd",
        theme=theme,
        is_playing=True,
    )
    save("spotify.svg", svg)

    print("Generating neural network map...")
    svg = neural_bezier_engine.generate_map(
        tech_stack={"Frontend": ["React", "Next.js"], "Backend": ["FastAPI", "Go"], "Infra": ["Docker", "K8s"]},
        theme=theme,
    )
    save("neural_map.svg", svg)

    print("Generating 3D globe...")
    svg = isometric_3d_globe.generate_globe(theme=theme)
    save("globe.svg", svg)

    print(f"\nAll outputs saved to: {OUTPUT_DIR}/")
    print("Open any .svg file in your browser to preview.\n")


if __name__ == "__main__":
    main()
