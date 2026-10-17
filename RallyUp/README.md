# RallyUp — Tennis XP

RallyUp is a small desktop app I made to keep track of tennis practice. I wanted it to do a bit more than store a list of sessions: after I log a practice, I can see the XP I earned, how close I am to the next level, and whether I have finished a task or unlocked a new title.

I kept it to one local player for now. I can enter a session quickly after practising, and the tasks give me a small reason to keep going the next day.

## What the app does

- Log a practice by entering the number of minutes and a training type. The list includes Serve, Forehand, Backhand, Footwork, Volley and Match Play, but I can type my own type too.
- Give 1 XP for each minute of practice. The next level needs more XP each time: 50 XP for the first level-up, then 75, 100, 125, and so on. Home has a progress bar for the current level.
- Track three short-term goals: 30 minutes today, 120 minutes this week, and three different training types this week. Tasks show progress, but do not give extra XP.
- Unlock seven achievements, including the first practice, five practices, 120 total minutes, three training types, 500 XP, and three-day and seven-day streaks. Each achievement has a title. Once unlocked, it stays unlocked.
- Show earlier practices in History, with pages when the list gets longer. Profile lets me change the player name and see my current level, XP and title.
- Show practice totals and two charts in Dashboard. Pandas adds up the data; Matplotlib draws the last seven days and the most-practised training types.

The form accepts a positive whole number of minutes and a non-blank training type. There is no account to create; the player and practice history are saved on this computer.

## Running it

I used Python 3.12. The extra packages are in `requirements.txt`. SQLite comes with Python, so there is no separate database server to set up. Start in the `RallyUp` folder, where `main.py` lives.

On macOS or Linux, run these commands the first time:

```bash
cd RallyUp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

On Windows, use:

```powershell
cd RallyUp
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If `RallyUp` is already the open folder in the terminal, skip `cd RallyUp`. On later launches, activate the same `.venv` and run `python main.py`; there is no need to reinstall the packages each time. A desktop display is needed because this is a windowed app.

## Finding my way around the files

`main.py` is the place to start reading. It sets up the database, opens the window and connects the seven menu buttons to their pages. When I click **Save Practice**, the path through the code is:

`ui/log_practice_page.py` → `database.py` → `xp_system.py` and `achievements.py` → feedback on the Log Practice page.

Here is what happens with an empty practice history if I enter **50 minutes of Serve** and press **Save Practice**:

1. `validate_practice()` checks that 50 is a positive whole number and that Serve is not blank. The page also reads the current task progress so it can tell whether this save finishes a task.
2. `save_practice()` writes the session to SQLite. In the same database transaction it adds 50 XP to the player, recalculates the level and checks for newly earned achievements. Keeping those writes together matters: if saving fails partway through, the XP should not get ahead of the practice history.
3. The form compares task progress before and after the save. It shows the XP, level-up, completed tasks and any new achievement in the message box. Home, History and Dashboard read the saved data when I open them.

The first level-up takes 50 XP, so that example reaches Level 2. Level 2 then needs 75 more XP; Level 3 needs 100 more. In `xp_system.py`, `caculate_level()` subtracts the XP already used for earlier levels. That is why Home can show **progress within this level**, instead of putting all-time XP directly into the progress bar.

| Path | What to look for |
| --- | --- |
| `main.py` | App startup and page switching. |
| `database.py` | SQLite tables, the local player and `save_practice()`. |
| `xp_system.py` | One XP per minute and the increasing level requirements. |
| `tasks.py` | The daily and weekly task calculations. |
| `achievements.py` | Achievement checks, titles and practice streaks. |
| `practice_stats.py` | Pandas summaries used by the charts. |
| `ui/home_page.py` | XP progress and a quick view of tasks. |
| `ui/log_practice_page.py` | The form, validation and save feedback. |
| `ui/tasks_page.py` | All three tasks and their progress bars. |
| `ui/history_page.py` | Saved sessions, newest first, four per page. |
| `ui/achievements_page.py` | Locked and unlocked achievements, three per page. |
| `ui/dashboard_page.py` | Summary cards and the two Matplotlib charts. |
| `ui/profile_page.py` | Player name and profile details. |
| `requirements.txt` | The packages installed with pip. |
| `data/rallyup.db` | The SQLite data file, created by the app. |

## Problems I ran into

**Keeping the XP rule easy to understand.** I considered giving different training types different XP, but then it would be harder to tell what a session was worth. For this first version I used 1 minute = 1 XP, so 30 minutes of Serve gives 30 XP. It also makes mistakes in the calculation easier for me to spot. A fixed XP target for every level felt too easy after a few sessions, so `xp4next_level()` starts at 50 and adds 25 for each later level. I found that Home could not use total XP directly for its progress bar: some of those points belong to levels already completed. `caculate_level()` works out both the level and the XP left within that level.

**Finding out where the records go.** I was unsure at first whether SQLite needed a separate server or whether closing the window would lose everything. This app uses Python's `sqlite3` and keeps the player, practices and unlocked achievements in `data/rallyup.db`. `init_db()` makes tables only when they are missing, so starting the app again does not wipe earlier sessions. In `save_practice()`, I put the new practice, total XP and achievement check inside one database transaction. That avoids having a saved practice with an old XP total if one part of the save fails.

**Tasks and achievements needed different rules.** I first thought the total practice time might be enough for the tasks, but that would let last week's training finish this week's goal. In `tasks.py`, I now check each practice date: the daily task counts today's minutes, and the weekly tasks count minutes and different training types from Monday to today. Achievements work differently. Once one is unlocked, I keep it in SQLite even when a new day or week starts. `achievements.py` checks the saved totals and streak; two sessions on one day count as one streak day. The unique user-and-achievement pair in the database stops a title being awarded twice. After a save, the form compares task progress before and after, so the player sees what this particular practice completed.

**Opening a page once did not catch the switching bug.** I had pages that looked fine alone, then disappeared or ended up too low after going Home → Log Practice → another page. The practice records were still there; the old page container was the problem. I also noticed text from another page flashing when I clicked the sidebar. In `main.py`, `show_multiPages()` now builds the next page first, places it over the old one, and only then destroys the old container. This matters most when the Dashboard needs a moment to draw its chart. I also removed an unnecessary forced refresh while building that page. I had to test the real sequence of clicks, not just whether each button opened something.

**The bottom of a long page could shake while scrolling.** I tried working on the mouse-wheel event first, but that did not fully match what I saw on screen. I changed the layout instead: Home, Log Practice, Tasks and Profile fit within the window; History and Achievements use Previous/Next pages; Dashboard shows one chart at a time. I checked the smallest allowed window, 760×560, and tightened the task cards when they took up too much height. I then checked the normal window size and switched through all seven modules again to make sure old containers were not piling up.

**Charts needed space as well as data.** `practice_stats.py` uses Pandas to add up minutes for the last seven days and by training type. It fills missing dates with zero, so a rest day still has a place on the chart. `ui/dashboard_page.py` uses Matplotlib to draw the results. Two charts stacked on one page made the small window awkward, so I changed it to a switch between “Last 7 days” and “Training types”. If there are no practices yet, the page shows a message instead of an empty graph.

If I need a backup, I close the app and copy `data/rallyup.db`.

## What is still simple

This version has one local player profile. It accepts whole minutes only, and there is no in-app button to edit or delete an old practice. Task targets are fixed, titles are chosen automatically, and the app does not judge practice quality or sync between computers.
