"""
Menubar and the parts of the menubar
    .
    App
    └── Root
        ├── Menubar
        ├── BaseFrame
        └── Statusbar
"""
from __future__ import annotations

import platform
import tkinter as tk
import typing

from biscuit import __version__
from biscuit.core.utils import Frame, IconButton, Label

from .item import MenubarItem

if typing.TYPE_CHECKING:
    from biscuit.core.components.floating import Menu

    from .. import Root


class Menubar(Frame):
    """
    Menubar of the application

    Attributes
    ----------
    master 
        Root window frame
    """
    def __init__(self, master: Root, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.menus: list[MenubarItem] = []
        self.events = self.base.commands

        # |-----left container-----|------searchbar------|------right container------|

        self.container = Frame(self, **self.base.theme.layout.menubar)
        self.container.pack(side=tk.LEFT, fill=tk.BOTH)

        from .searchbar import Searchbar
        self.searchbar = Searchbar(self)
        self.searchbar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.container_right = Frame(self, **self.base.theme.layout.menubar)
        self.container_right.pack(side=tk.RIGHT, fill=tk.BOTH)

        # make this custom titlebar for windows
        if platform.system() == 'Windows':
            close = IconButton(self.container_right, icon='chrome-close', iconsize=12, padx=15, pady=8, event=self.events.quit)
            close.config(activebackground='#e81123', activeforeground="white")
            close.pack(side=tk.RIGHT, fill=tk.Y, padx=0)

            IconButton(self.container_right, icon='chrome-maximize', iconsize=12, icon2='chrome-restore', padx=15, pady=8, event=self.events.toggle_maximize).pack(side=tk.RIGHT, fill=tk.Y, padx=0)
            IconButton(self.container_right, icon='chrome-minimize', iconsize=12, padx=15, pady=8, event=self.events.minimize).pack(side=tk.RIGHT, fill=tk.Y, padx=0)
            self.config_bindings()
        
        self.update_idletasks()

        self.config(**self.base.theme.layout.menubar)
        self.add_menus()
    
    def change_title(self, title: str) -> None:
        self.searchbar.label.change_text(title)

    def config_bindings(self) -> None:
        self.bind('<Map>', self.events.window_mapped)
        self.bind("<Button-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.moving)

    def start_move(self, event) -> None:
        self.x = event.x
        self.y = event.y

    def stop_move(self, _) -> None:
        self.x = None
        self.y = None

    def moving(self, event: tk.Event) -> None:
        x = (event.x_root - self.x)
        y = (event.y_root - self.y)
        self.base.geometry(f"+{x}+{y}")

    def add_menu(self, text: str) -> Menu:
        new_menu = MenubarItem(self.container, text)
        new_menu.pack(side=tk.LEFT, fill=tk.BOTH)
        self.menus.append(new_menu)

        return new_menu.menu

    def add_menus(self) -> None:
        #TODO menu shall support check items
        self.add_file_menu()
        self.add_edit_menu()
        self.add_selection_menu()
        self.add_view_menu()
        self.add_go_menu()
        self.add_help_menu()

    def add_file_menu(self) -> None:
        events = self.events

        self.file_menu = self.add_menu("File")
        self.file_menu.add_item("New File", events.new_file)
        self.file_menu.add_item("New Window", events.new_window)
        self.file_menu.add_separator()
        self.file_menu.add_item("Open File", events.open_file)
        self.file_menu.add_item("Open Folder", events.open_directory)
        self.file_menu.add_item("Open Recent File...", events.open_recent_file)
        self.file_menu.add_item("Open Recent Folder...", events.open_recent_dir)
        self.file_menu.add_separator()
        self.file_menu.add_item("Save", events.save)
        self.file_menu.add_item("Save As...", events.save_as)
        self.file_menu.add_item("Save All", events.save_all)
        self.file_menu.add_separator()
        self.file_menu.add_item("Preferences", events.open_settings)
        self.file_menu.add_separator()
        self.file_menu.add_item("Close Editor", events.close_file)
        self.file_menu.add_item("Close Folder", events.close_dir)
        self.file_menu.add_item("Close Window", events.quit)
        self.file_menu.add_separator()
        self.file_menu.add_item("Exit", events.quit)

    def add_edit_menu(self) -> None:
        events = self.events

        self.edit_menu = self.add_menu("Edit")
        self.edit_menu.add_item("Undo", events.undo)
        self.edit_menu.add_item("Redo", events.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_item("Cut", events.cut)
        self.edit_menu.add_item("Copy", events.copy)
        self.edit_menu.add_item("Paste", events.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_item("Find", events.find)
        self.edit_menu.add_item("Replace", events.replace)
        self.edit_menu.add_item("Find in Files", events.show_file_search)
        self.edit_menu.add_item("Change Language Mode", events.change_language_mode)
        self.edit_menu.add_separator()
        self.edit_menu.add_checkable("Word Wrap", events.toggle_wordwrap)
        self.edit_menu.add_checkable("Block Cursor", events.toggle_block_cursor)

    def add_selection_menu(self) -> None:
        events = self.events

        self.selection_menu = self.add_menu("Selection")
        self.selection_menu.add_item("Select All", events.select_all)
        self.selection_menu.add_item("Select Line", events.select_line)
        self.selection_menu.add_item("Delete Line", events.delete_line)
        self.selection_menu.add_separator()
        self.selection_menu.add_item("Copy Line Up", events.copy_line_up)
        self.selection_menu.add_item("Copy Line Down", events.copy_line_down)
        self.selection_menu.add_item("Move Line Up", events.move_line_up)
        self.selection_menu.add_item("Move Line Down", events.move_line_down)
        self.selection_menu.add_item("Duplicate Selection", events.duplicate_selection)

    def add_view_menu(self) -> None:
        events = self.events

        self.view_menu = self.add_menu("View")
        self.view_menu.add_item("Command Palette...", events.show_command_palette)
        self.view_menu.add_item("Explorer", events.show_explorer)
        self.view_menu.add_item("Outline", events.show_outline)
        self.view_menu.add_item("Search", events.show_search)
        self.view_menu.add_item("Source Control", events.show_source_control)
        self.view_menu.add_item("Extensions", events.show_extensions)
        self.view_menu.add_separator()
        self.view_menu.add_item("Terminal", events.show_terminal)
        self.view_menu.add_item("Log", events.show_logs)

    def add_go_menu(self) -> None:
        events = self.events

        self.view_menu = self.add_menu("Go")
        self.view_menu.add_item("Go to File...", events.show_file_search)
        self.view_menu.add_separator()
        self.view_menu.add_item("Go to Symbol in Editor", events.show_symbol_palette)
        self.view_menu.add_item("Go to Definition", events.go_to_definition)
        self.view_menu.add_item("Go to References", events.find_references)
        self.view_menu.add_separator()
        self.view_menu.add_item("Go to Line/Column...", events.show_goto_palette)
    
    def add_help_menu(self) -> None:
        events = self.events

        self.help_menu = self.add_menu("Help")
        self.help_menu.add_item("Welcome", events.show_welcome)
        self.help_menu.add_item("Show All Commands", events.show_command_palette)
        self.help_menu.add_item("Documentation", events.documentation)
        self.help_menu.add_item("Show Release Notes", events.release_notes)
        self.help_menu.add_separator()
        self.help_menu.add_item("Report Bug", events.report_bug)
        self.help_menu.add_item("Request Feature", events.request_feature)
        self.help_menu.add_separator()
        self.help_menu.add_item("View License", events.view_license)
        self.help_menu.add_item("Code of Conduct", events.code_of_conduct)
        self.help_menu.add_separator()
        self.help_menu.add_item("About", events.about)

    def close_all_menus(self, *_) -> None:
        for btn in self.menus:
            btn.menu.hide()

    def switch_menu(self, item: MenubarItem) -> None:
        active = False
        for i in self.menus:
            if i.menu.active:
                active = True
            if i.menu != item.menu:
                i.menu.hide()
                i.deselect()

        if active:
            item.select()
            item.menu.show()
