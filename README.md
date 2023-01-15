# git-glyph-timelapse

This tool converts the git history of Glyphs .glyph files (Glyphspackage format) into an animation using DrawBot.

![Animated "s"](https://user-images.githubusercontent.com/5319916/212504691-6e5db4b5-6e5c-4c8f-b6d7-b250431fef80.gif)

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

### Current limitations (things to fix, decide not to fix, or create issues for):
- Probably doesn't work on public repos
- Doesn't support .glyphs, only .glyphspackage
- Does not work if there are components in the glyph you specify
- Does not work if glyph nodes have special metadata, e.g. if you use the LTTR/INK plugin
- Does not support UFO (could generalize this to support `.glif` as well)
- Code is a mess!

### Things to refactor:
- Instead of using the GitHub API, generalize this to work with local git; for GitHub support, optionally clone a remote repo that you have permission to. This will transfer more data but create far fewer network requests when requesting glyphs vs. loading them directly from a local git repo. 

Free, without warranty software. Not responsible for etc.!
