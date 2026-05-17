import os
import subprocess
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
REPO_NAME = "history-experiment-2015"
YEAR = 2015

def create_commit(date):
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Set the fake dates for Git
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Change a file to ensure a unique hash
    with open("timeline.txt", "a") as f:
        f.write(f"Entry for {date_str} - hash salt: {random.randint(0, 100000)}\n")
    
    subprocess.run(["git", "add", "timeline.txt"], check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"Refactor for {date_str}"],
        env=env,
        check=True,
        capture_output=True
    )

def main():
    # 1. Setup local directory
    if not os.path.exists(REPO_NAME):
        os.makedirs(REPO_NAME)
    os.chdir(REPO_NAME)
    
    # 2. Initialize Git
    subprocess.run(["git", "init"], check=True)
    
    # 3. Iterate through every day of the year
    start_date = datetime(YEAR, 1, 1)
    end_date = datetime(YEAR, 12, 31)
    current_date = start_date

    print(f"🚀 Generating 2015 history in {REPO_NAME}...")

    while current_date <= end_date:
        # Determine density: Weekends lighter, Weekdays heavier
        # 0=Monday, 6=Sunday
        weekday = current_date.weekday()
        
        if weekday >= 5: # Weekend
            commits_today = random.randint(1, 3) 
        else: # Weekday
            commits_today = random.randint(3, 8)

        # Optional: Add a "Linus Spike" every 8 weeks
        if current_date.timetuple().tm_yday % 60 < 7:
            commits_today = 25 

        for _ in range(commits_today):
            create_commit(current_date)
            
        current_date += timedelta(days=1)

    print("\n✅ Local repository ready!")
    print("-" * 30)
    print("FINAL STEPS:")
    print(f"1. Create a NEW repo on GitHub named '{REPO_NAME}'")
    print(f"2. git remote add origin https://github.com/akgamerz790/{REPO_NAME}.git")
    print("3. git branch -M main")
    print("4. git push -u origin main")
    print("-" * 30)
    print("💡 TO REVERT: Just delete the repository on GitHub.")

if __name__ == "__main__":
    main()