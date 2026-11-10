# Historical Atlas r37 sources

These are **retained build dependencies** for Atlas 40. The current Atlas 40 source under [atlas39](../atlas39/) reads `atlas37/template.html`, `atlas37/sprites.py` and locally produced `atlas37/data.json` and `atlas37/images.json`.

The generated 16-map HTML viewer, exports and obsolete scripts formerly in `atlas/` were retired from current `main` after Atlas 40 became a standalone package. They remain accessible in [the pre-cleanup Git revision](https://github.com/Valetos2/Cyber-Cop-Genesis-mod/tree/1edde6660f9962bf161f645d7b2da42eb98d16c2/atlas).

If historical r37 HTML is regenerated locally, the renderer writes to `atlas37/`. Run `node atlas37/test_ui.js` and `node atlas37/test_state.js` after generating those HTML files. Private original ROMs and research fixtures are required for generation and are not published here.
