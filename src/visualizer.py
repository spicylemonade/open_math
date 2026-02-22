"""Terminal-based visualization for cellular automata.

Provides real-time rendering using Unicode block characters,
with interactive controls (pause, step, quit) via curses.
Falls back to plain-text mode in environments without curses.
"""

import sys
import time


# Unicode block characters for 2x1 cell rendering
BLOCK_CHARS = {
    (0, 0): " ",
    (1, 0): "\u2580",  # upper half block
    (0, 1): "\u2584",  # lower half block
    (1, 1): "\u2588",  # full block
}


def render_unicode(grid):
    """Render a grid using Unicode half-block characters.

    Each character represents 2 rows (top and bottom halves).

    Args:
        grid: Grid or NumPyGrid instance.

    Returns:
        List of strings, one per display row.
    """
    lines = []
    for y in range(0, grid.height, 2):
        line = ""
        for x in range(grid.width):
            top = grid.get(x, y)
            bottom = grid.get(x, y + 1) if y + 1 < grid.height else 0
            line += BLOCK_CHARS[(top, bottom)]
        lines.append(line)
    return lines


def render_plain(grid):
    """Render a grid using plain ASCII characters.

    Args:
        grid: Grid or NumPyGrid instance.

    Returns:
        List of strings.
    """
    lines = []
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):
            line += "O" if grid.get(x, y) else "."
        lines.append(line)
    return lines


def run_plain_text(simulator, fps=10, max_frames=None):
    """Run simulation with plain-text output.

    Prints each frame to stdout. Suitable for non-interactive environments.

    Args:
        simulator: Simulator instance.
        fps: Frames per second.
        max_frames: Maximum frames to display (None for unlimited).
    """
    delay = 1.0 / fps
    frame = 0
    try:
        while max_frames is None or frame < max_frames:
            lines = render_unicode(simulator.grid)
            sys.stdout.write(f"\033[2J\033[H")  # clear screen
            sys.stdout.write(f"Generation: {simulator.generation}  "
                           f"Population: {simulator.grid.population()}\n")
            sys.stdout.write("\n".join(lines) + "\n")
            sys.stdout.flush()
            time.sleep(delay)
            simulator.step()
            frame += 1
    except KeyboardInterrupt:
        pass


def run_curses(simulator, fps=10):
    """Run simulation with curses-based interactive display.

    Controls:
        Space: pause/resume
        Right arrow: single step (when paused)
        Q/Esc: quit

    Args:
        simulator: Simulator instance.
        fps: Target frames per second.
    """
    try:
        import curses
    except ImportError:
        print("curses not available, falling back to plain-text mode")
        run_plain_text(simulator, fps)
        return

    def _main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(int(1000 / fps))

        paused = False
        running = True

        while running:
            # Render
            stdscr.erase()
            lines = render_unicode(simulator.grid)
            max_y, max_x = stdscr.getmaxyx()

            status = (f"Gen: {simulator.generation}  "
                     f"Pop: {simulator.grid.population()}  "
                     f"{'[PAUSED]' if paused else '[RUNNING]'}  "
                     f"Space=pause  Arrow=step  Q=quit")
            try:
                stdscr.addstr(0, 0, status[:max_x - 1])
            except curses.error:
                pass

            for i, line in enumerate(lines):
                if i + 1 >= max_y:
                    break
                try:
                    stdscr.addstr(i + 1, 0, line[:max_x - 1])
                except curses.error:
                    pass

            stdscr.refresh()

            # Handle input
            key = stdscr.getch()
            if key == ord("q") or key == 27:  # Q or Esc
                running = False
            elif key == ord(" "):
                paused = not paused
            elif key == curses.KEY_RIGHT and paused:
                simulator.step()
            elif not paused:
                simulator.step()

    curses.wrapper(_main)


def run_visualizer(simulator, fps=10, mode="auto", max_frames=None):
    """Run the visualizer with automatic mode detection.

    Args:
        simulator: Simulator instance.
        fps: Target frames per second.
        mode: 'curses', 'plain', or 'auto' (try curses, fall back to plain).
        max_frames: For plain mode, max frames to display.
    """
    if mode == "curses":
        run_curses(simulator, fps)
    elif mode == "plain":
        run_plain_text(simulator, fps, max_frames)
    else:
        # Auto-detect
        if sys.stdout.isatty():
            try:
                import curses
                run_curses(simulator, fps)
            except (ImportError, curses.error):
                run_plain_text(simulator, fps, max_frames)
        else:
            run_plain_text(simulator, fps, max_frames)
