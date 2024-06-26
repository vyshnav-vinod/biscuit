import tkinter as tk

from biscuit.core.utils import IconLabelButton


class CheckableMenuItem(IconLabelButton):
    def __init__(self, master, text, command=lambda *_:..., checked=False, *args, **kwargs) -> None:
        super().__init__(master, text, 'check', command, expandicon=False, iconsize=10, toggle=False, *args, **kwargs)

        self.command = command
        if checked:
            self.toggle_icon()
            
        self.bg, self.fg, self.hbg, self.hfg = self.base.theme.menu.item.values()
        self.on_leave()

    def on_click(self, *_) -> None:
        self.master.hide()
        self.toggle_icon()
        return super().on_click(*_)

