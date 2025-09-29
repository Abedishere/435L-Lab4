"""
Small launcher.

Default: run the Tk/ttk app.
You can still call: python start.py --tk
"""

import sys

def main() -> None:
    use_tk = ("--tk" in sys.argv) or True  # always Tk for this lab
    if use_tk:
        from apptk import main as run
        run()
    else:
        # kept for parity; we don't ship a Qt variant in this lab
        from apptk import main as run
        run()
if __name__ == "__main__":


    main()
