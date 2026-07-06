# cursor-setup-task
100Hires 1st Task

## Tools installed
- Cursor IDE
- Claude Code Extension (within Cursor)
- Codex Extension (within Cursor)

## Completed Steps
- Installed Cursor IDE application
- Installed Claude Code Extension 
- Installed Codex Extension
- Login to both Claude Code and Codex
- Created a public Github repository
- Cloned(as it is needed to access it from local files) and opened the repository within Cursor

## Issues Encountered
- Could not find Extensions panel in Cursor due to Agent UI mode (first time installed)
- Login into Claude Code and Codex
- Check if im logged in to Claude Code and Codex
- Unable to commit README.md due to an error "user.name" and "user.email" in git

## Solutions
- Used Command Palette (Ctrl + Shift + P) to switch into Editor mode
- Used Command Palette (Ctrl + Shift + X) to access extension
- Used Command Palette (Ctrl + Shift + P) to access Claude Code and login to Anthropic using Gmail
- Used Command Palette (Ctrl + Shift + P) to access Codex and login using ChatGPT account
- Try using a dummy project and use the extensions to check if the extensions is connected (Claude Code and Codex)
- Use Terminal in Cursor to set name and email for Git  
[git config --global user.name "Name"]
[git config --global user.email "email@email.com"]

## Notes
- Codex extension worked successfully after opening other project for testing
- Claude Code installation was successful, but usage was unavailable due to lack of credits/balance

---

## Project Overview

This repository contains a structured research project on AI-powered SEO content production.  

The goal of this project is to:
- Identify high-quality SEO experts actively working in the field  
- Collect and organize their insights (LinkedIn posts, content)  
- Build a dataset that can later be used to develop a real-world SEO playbook

---

## What Was Collected

The following research materials were collected:

- LinkedIn posts from selected SEO experts  
- Insights on AI-driven content workflows  
- Strategies related to SEO content scaling and automation  
- Supporting materials (where available)

All data is organized inside:
/research  
|--- sources.md  
|--- linkedin-posts/  
|--- youtube-transcripts/  

Each LinkedIn post is structured with:
- Author  
- Source link  
- Post content  
- Key takeaways  

---

## Why These Experts Were Chosen

The selected experts were chosen based on:

- Active involvement in SEO and content strategy  
- Proven experience in real-world SEO implementation  
- Relevance to AI-powered content workflows  
- Consistent sharing of actionable insights (not just theory)

The dataset includes experts from different areas of SEO:

- SEO Strategy & Growth (e.g., Kevin Indig, Neil Patel)  
- Technical SEO (e.g., Aleyda Solis, Patrick Stox)  
- Content & Distribution (e.g., Ross Simmonds)  
- Search Trends & Analysis (e.g., Lily Ray, Rand Fishkin)

This ensures a balanced perspective across both:
- content creation  
- and search engine behavior  

---

## Repository Structure

/research  
|--- sources.md ##Curated list of SEO experts with annotations  
|--- linkedin-posts/ ##Posts organized by author  
|--- youtube-transcripts/ ##Transcripts collected via script (where available)  
|--- other/ ##Additional materials (if any)

/scripts  
|--- youtube_fetcher.py #Script to fetch YouTube transcripts

---

## Tools & Technologies

- Cursor IDE  
- Claude Code (within Cursor)  
- Codex (within Cursor)  
- Python  
- youtube-transcript-api  

---

## Data Collection Approach

### LinkedIn Posts
- Manually collected from selected experts  
- Focused on recent and relevant posts  
- Extracted key insights for analysis  

### YouTube Transcripts
- Attempted using 'youtube-transcript-api'  
- Limited by subtitle availability  

---

## Challenges Encountered

- Many YouTube videos did not provide transcripts
- Transcript extraction fails and cause code to be terminated/stop working 
- Cursor usage limits restricted automation

---

## Solutions

- Switched to manual LinkedIn data collection 
- Use cursor AI to fix the code and add automation for each failed transcript extraction to be skipped and asked for the transcript to have metadata 
- Prioritized high-quality sources over volume 

---

## Outcome

This repository represents:
- A structured SEO research dataset  
- Organized expert insights  
- A foundation for building an AI SEO content strategy  

---