#!/usr/bin/python3
import curses

if __name__ == '__main__':
    curses.initscr()

    window = curses.newwin(15, 40, 7, 20)
    window.box()
    window.refresh()

    subwindow = window.derwin(5, 10, 2, 2)  # <- here is the change
    subwindow.box()
    subwindow.refresh()

    subwindow.getkey()

    curses.endwin()
    