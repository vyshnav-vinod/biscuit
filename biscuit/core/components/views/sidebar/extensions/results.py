import json
import queue
import threading
import tkinter as tk

import requests

from biscuit.core.utils.scrollableframe import ScrollableFrame

from ..item import SidebarViewItem
from .extension import Extension
from .placeholder import ExtensionsPlaceholder
from .watcher import ExtensionsWatcher


class Results(SidebarViewItem):
    def __init__(self, master, *args, **kwargs) -> None:
        self.__buttons__ = ()
        self.title = 'Available'
        super().__init__(master, *args, **kwargs)
        self.config(**self.base.theme.views.sidebar.item)

        self.extensions = {}

        self.placeholder = ExtensionsPlaceholder(self)
        self.extension_list = ScrollableFrame(self.content, bg=self.base.theme.views.sidebar.background)
        self.extension_list.pack(fill=tk.BOTH, expand=True)

        self.repo_url = "https://raw.githubusercontent.com/tomlin7/biscuit-extensions/main/"
        self.list_url = self.repo_url + "extensions.json"

        self.queue = queue.Queue()

        # self.watcher = ExtensionsWatcher(self)
        # self.watcher.watch()

        #TODO list installed extensions separately

        self.fetching = threading.Event()
        self.extensions_lock = threading.Lock()

    def refresh(self, *_) -> None:
        if self.base.testing:
            return

        self.clear()
        self.update_idletasks()
        self.after(5, self.run_fetch_list())

    def run_fetch_list(self, *_) -> None:
        if self.base.testing:
            return

        if self.fetching.is_set():
            self.fetching.wait()

        with self.extensions_lock: 
            threading.Thread(target=self.fetch_list, daemon=True).start()

    def fetch_list(self) -> None:
        response = None
        try:
            response = requests.get(self.list_url)
        except Exception as e:
            pass
            
        # FAIL - network error
        if not response or response.status_code != 200:
            self.extension_list.pack_forget()
            self.placeholder.pack(in_=self.content, fill=tk.BOTH, expand=True)
            return
        
        self.extensions = json.loads(response.text)
        # SUCCESS
        if self.extensions:
            self.placeholder.pack_forget()
            self.extension_list.pack(in_=self.content, fill=tk.BOTH, expand=True)

        for name, data in self.extensions.items():
            #TODO add further loops for folders
            self.queue.put((name, data))
    
    def gui_refresh_loop(self) -> None:
        if not self.queue.empty():
            name, data = self.queue.get()
            ext = Extension(self, name, data)
            self.extension_list.add(ext, fill=tk.X)
        
        self.after(5, self.gui_refresh_loop)

    def clear(self, *_) -> None:
        for widget in self.extension_list.items:
            widget.pack_forget()
            widget.destroy()
            self.content.update_idletasks()

        self.fetching.set()
