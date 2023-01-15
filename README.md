# git-glyph-timelapse

This tool converts the git history of Glyphs .glyph files (Glyphspackage) into an animation using DrawBot.

To install, make sure DrawBot has `openstep_plist`, `requests` and `base64` python packages installed. To use, modify these variables in `index.py` and run:

```
REPO_OWNER_NAME = "org-or-username"
REPO_NAME = "repo-name"
GLYPHSPACKAGE_PATH = "MyFont.glyphspackage"
TOKEN = "a_github_token_with_repo_permission"
OUTLINE_MODE = True
GLYPH_NAME = "S"
MASTER_IDX = 1  # 0 for single master
SAVE_DIR = "~/Desktop"
SAVE_FORMAT = "mp4"
```

### Current limitations:
- Does not work if there are components in the glyph you specify (to do, PRs welcome)
- Does not work if glyph nodes have special metadata, e.g. if you use the LTTR/INK plugin
- Does not support UFO (could generalize this to support `.glif` as well)
- Code is a mess!

Free, without warranty software. Not responsible for etc.