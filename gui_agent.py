"""Simple GUI popup for the concise-answer agent using tkinter.

Features:
- Single-window popup with input box and Ask button
- Shows brief answer and source link (clickable)
- Runs queries in a background thread to keep UI responsive
"""
import threading
import queue
import webbrowser
import tkinter as tk
from tkinter import ttk
from typing import Optional

try:
    from agent import answer_query
except Exception:
    # Fallback: import from main via agent import chain
    from agent import answer_query


class AgentGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Concise AI Agent")
        root.geometry("600x320")

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        self.entry = ttk.Entry(frm)
        self.entry.pack(fill=tk.X, pady=(0, 8))
        self.entry.bind('<Return>', lambda e: self.on_ask())

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X)
        self.ask_btn = ttk.Button(btn_frame, text="Ask", command=self.on_ask)
        self.ask_btn.pack(side=tk.LEFT)
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.on_clear)
        self.clear_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.status = ttk.Label(frm, text="Ready", foreground="gray")
        self.status.pack(fill=tk.X, pady=(8, 8))

        self.output = tk.Text(frm, height=10, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.configure(state=tk.DISABLED)

        self.src_link = ttk.Label(frm, text="", foreground="blue", cursor="hand2")
        self.src_link.pack(anchor='w', pady=(6, 0))
        self.src_link.bind('<Button-1>', self._open_source)

        self._q: queue.Queue = queue.Queue()
        self._source_url: Optional[str] = None

        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Poll queue for results
        self._poll()

    def on_clear(self):
        self.entry.delete(0, tk.END)
        self._set_output('')
        self.src_link.config(text='')

    def on_ask(self):
        query = self.entry.get().strip()
        if not query:
            return
        self.ask_btn.config(state=tk.DISABLED)
        self.status.config(text="Thinking...", foreground="orange")
        threading.Thread(target=self._worker, args=(query,), daemon=True).start()

    def _worker(self, query: str):
        try:
            ans, src = answer_query(query)
            self._q.put((ans, src))
        except Exception as e:
            self._q.put((f"Error: {e}", None))

    def _poll(self):
        try:
            ans, src = self._q.get_nowait()
        except queue.Empty:
            self.root.after(100, self._poll)
            return

        self._set_output(ans)
        if src:
            self._source_url = src
            self.src_link.config(text=f"Source: {src}")
        else:
            self._source_url = None
            self.src_link.config(text='')

        self.status.config(text="Ready", foreground="green")
        self.ask_btn.config(state=tk.NORMAL)
        self.root.after(100, self._poll)

    def _set_output(self, text: str):
        self.output.configure(state=tk.NORMAL)
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def _open_source(self, event=None):
        if self._source_url:
            try:
                webbrowser.open(self._source_url)
            except Exception:
                pass

    def on_close(self):
        try:
            self.root.destroy()
        except Exception:
            pass


def main():
    root = tk.Tk()
    gui = AgentGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
