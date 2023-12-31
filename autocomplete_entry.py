import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._autocompleteList = sorted(autocompleteList)
        self._hits = []
        self._hitIndex = 0
        self.position = 0
        self.bind("<KeyRelease>", self.handle_keyrelease)
        self['exportselection'] = False

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())

        _hits = []
        for element in self._autocompleteList:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)

        if _hits != self._hits:
            self._hitIndex = 0
            self._hits = _hits

        if _hits == self._hits and _hits:
            self._hitIndex = (self._hitIndex + delta) % len(_hits)

        if _hits:
            self.delete(0, tk.END)
            self.insert(0, _hits[self._hitIndex])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)
        if len(event.keysym) == 1:
            self.autocomplete()