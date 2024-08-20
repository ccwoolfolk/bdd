# Terminal recording to .gif

The video uses `asciinema` to record a terminal session and `asciinema/agg` to convert the recording to a .gif. `tmux` can make this a bit easier. Create a new session, get the panes set, etc. then detach.

```bash
asciinema rec --command "tmux attach" bdd-demo.cast
```

Detach when you're done. (`Ctrl-b d`)

To generate the gif, you'll need to install `asciinema/agg`. On WSL, installing via Homebrew was easiest.

```bash
 agg --cols 95 --rows 45 --theme dracula ./bdd-demo.cast /mnt/c/Users/path-to-your-project/bdd-demo.gif --font-dir=.
 ```

## Resources

- https://github.com/asciinema/asciinema
- https://github.com/asciinema/agg
- https://nixdaily.com/how-to/record-your-terminal-session-and-convert-it-to-a-gif-image-asciinema/
- https://github.com/asciinema/asciinema/wiki/Recording-tmux-session
