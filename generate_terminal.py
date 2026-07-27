import gifos
from datetime import datetime
import os
import requests

USERNAME = (
    os.environ.get("GIT_USERNAME")
    or os.environ.get("GITHUB_REPOSITORY_OWNER")
    or "muhammad-awais-web-dev"
)

def get_total_repos(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            return response.json().get("public_repos", 0)
    except:
        pass
    return None

try:
    github_stats = gifos.utils.fetch_github_stats(user_name=USERNAME)
    has_stats = github_stats is not None
except Exception as e:
    print(f"Warning: Error fetching GitHub stats: {e}")
    has_stats = False
    github_stats = None

total_repos = get_total_repos(USERNAME)

t = gifos.Terminal(width=710, height=480, xpad=15, ypad=15)
t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[94mgithub\x1b[0m ~> ")

# Boot Sequence
t.gen_text("Booting GIF_OS v1.1.0...", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m Network connection established", row_num=2)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m Fetching profile metrics", row_num=3)
t.clone_frame(10)

t.gen_prompt(row_num=4)
t.gen_typing_text("neofetch --user " + USERNAME, row_num=4, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=5)
t.gen_text(f"\x1b[96m=== Muhammad Awais Profile ===\x1b[0m", row_num=6)
t.clone_frame(3)

if has_stats:
    repos_count = total_repos if total_repos else github_stats.total_repo_contributions
    stats_lines = [
        f"\x1b[93mName:\x1b[0m        {github_stats.account_name or USERNAME}",
        f"\x1b[93mRole:\x1b[0m        Full-Stack Web Developer",
        f"\x1b[93mFollowers:\x1b[0m   {github_stats.total_followers}",
        f"\x1b[93mStars:\x1b[0m       {github_stats.total_stargazers}",
        f"\x1b[93mCommits:\x1b[0m     {github_stats.total_commits_last_year} (last year)",
        f"\x1b[93mPRs:\x1b[0m         {github_stats.total_pull_requests_made}",
        f"\x1b[93mRepos:\x1b[0m       {repos_count}",
        f"\x1b[93mRank:\x1b[0m        {github_stats.user_rank.level} ({github_stats.user_rank.percentile:.1f}%)",
    ]
    
    if github_stats.languages_sorted:
        top_langs = github_stats.languages_sorted[:3]
        langs_str = ", ".join([f"{lang[0]} ({lang[1]}%)" for lang in top_langs])
        stats_lines.append(f"\x1b[93mTop Langs:\x1b[0m   {langs_str}")
else:
    stats_lines = [
        f"\x1b[93mName:\x1b[0m        {USERNAME}",
        "\x1b[93mRole:\x1b[0m        Full-Stack Web Developer",
        "\x1b[93mFollowers:\x1b[0m   --",
        "\x1b[93mStars:\x1b[0m       --",
        "\x1b[93mCommits:\x1b[0m     --",
        "\x1b[93mPRs:\x1b[0m         --",
        "\x1b[93mRepos:\x1b[0m       --",
        "\x1b[93mRank:\x1b[0m        --",
    ]

for i, line in enumerate(stats_lines):
    t.gen_text(line, row_num=7+i)
    t.clone_frame(3)

t.clone_frame(10)
t.gen_text("\x1b[96m==============================\x1b[0m", row_num=7+len(stats_lines))
t.clone_frame(15)

# Clear and Tech Stack
t.gen_prompt(row_num=8+len(stats_lines))
t.gen_typing_text("clear", row_num=8+len(stats_lines), contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat tech_skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m=== Tech Stack ===\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94mFront-End:\x1b[0m   ", "React, Next.js, TypeScript, Tailwind CSS"),
    ("\x1b[94mBack-End:\x1b[0m    ", "Node.js, Python, Django, WordPress"),
    ("\x1b[94mAutomation:\x1b[0m  ", "n8n, WooCommerce, REST APIs"),
    ("\x1b[94mTools:\x1b[0m       ", "Figma, Git, GitHub, Vercel"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text("\x1b[96m==================\x1b[0m", row_num=4+len(skills))
t.clone_frame(5)

# Final message
final_row = 5 + len(skills)
t.gen_prompt(row_num=final_row)
t.gen_typing_text("echo 'Welcome to my GitHub profile!'", row_num=final_row, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[92mWelcome to my GitHub profile!\x1b[0m", row_num=final_row+1)
t.clone_frame(40)

# Save to terminal.gif
t.gen_gif()
if os.path.exists("output.gif"):
    if os.path.exists("terminal.gif"):
        os.remove("terminal.gif")
    os.rename("output.gif", "terminal.gif")
