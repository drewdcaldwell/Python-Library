
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ------- LaTeX escaping helpers -------
LATEX_SPECIALS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}

def latex_escape(text: str) -> str:
    """Escape LaTeX special characters in text."""
    if not text:
        return ""
    out = []
    for ch in text:
        out.append(LATEX_SPECIALS.get(ch, ch))
    return "".join(out)

def sanitize_key(key: str) -> str:
    """Keys must be simple: letters, digits, dash/underscore. No spaces."""
    key = key.strip()
    key = key.replace(" ", "_")
    # Optionally, remove disallowed characters
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return "".join(ch for ch in key if ch in allowed)

# ------- LaTeX snippet generator -------

def make_glossary_entry(key, name, symbol, user1, plural, description):
    """
    Returns a formatted \newglossaryentry snippet.
    Only includes optional fields if provided.
    """
    key = sanitize_key(key)
    name = latex_escape(name.strip())
    symbol = latex_escape(symbol.strip())
    user1 = latex_escape(user1.strip())
    plural = latex_escape(plural.strip())
    description = latex_escape(description.strip())

    if not key:
        raise ValueError("Key is required.")
    if not name:
        raise ValueError("Name (the word) is required.")
    if not description:
        raise ValueError("Description is required.")

    # Build lines conditionally (note the escaped braces in f-strings):
    fields = [f"  name={{{name}}}"]
    if symbol:
        fields.append(f"  symbol={{{symbol}}}")
    if user1:
        fields.append(f"  user1={{{user1}}}")
    if plural:
        fields.append(f"  plural={{{plural}}}")
    fields.append(f"  description={{{description}}}")

    body = ",\n".join(fields)
    snippet = f"\\newglossaryentry{{{key}}}{{\n{body}\n}}\n"
    return snippet


# ------- GUI -------
class GlossaryEntryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LaTeX Glossary Entry Maker")
        self.geometry("820x620")
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Labels & entries
        row = 0
        ttk.Label(frm, text="Key (unique, no spaces):").grid(row=row, column=0, sticky="w")
        self.key_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.key_var, width=40).grid(row=row, column=1, sticky="we", padx=6)

        row += 1
        ttk.Label(frm, text="Name (word):").grid(row=row, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.name_var, width=40).grid(row=row, column=1, sticky="we", padx=6)

        row += 1
        ttk.Label(frm, text="Pronunciation (symbol):").grid(row=row, column=0, sticky="w")
        self.symbol_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.symbol_var, width=40).grid(row=row, column=1, sticky="we", padx=6)

        row += 1
        ttk.Label(frm, text="Part of Speech (user1):").grid(row=row, column=0, sticky="w")
        self.user1_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.user1_var, width=40).grid(row=row, column=1, sticky="we", padx=6)

        row += 1
        ttk.Label(frm, text="Plural (optional):").grid(row=row, column=0, sticky="w")
        self.plural_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.plural_var, width=40).grid(row=row, column=1, sticky="we", padx=6)

        row += 1
        ttk.Label(frm, text="Description:").grid(row=row, column=0, sticky="nw")
        self.desc_txt = tk.Text(frm, width=60, height=8, wrap="word")
        self.desc_txt.grid(row=row, column=1, sticky="we", padx=6)

        # Buttons
        row += 1
        btns = ttk.Frame(frm)
        btns.grid(row=row, column=0, columnspan=2, pady=8, sticky="we")
        ttk.Button(btns, text="Generate", command=self.on_generate).pack(side="left", padx=4)
        ttk.Button(btns, text="Copy to Clipboard", command=self.on_copy).pack(side="left", padx=4)
        ttk.Button(btns, text="Append to .tex File...", command=self.on_append_file).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.on_clear).pack(side="left", padx=4)

        # Preview
        row += 1
        ttk.Label(frm, text="Preview:").grid(row=row, column=0, sticky="w", pady=(8, 2))
        self.preview_txt = tk.Text(frm, width=100, height=14, wrap="none")
        self.preview_txt.grid(row=row, column=0, columnspan=2, sticky="nsew")
        frm.rowconfigure(row, weight=1)
        frm.columnconfigure(1, weight=1)

        # Status
        row += 1
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(frm, textvariable=self.status_var, foreground="#555").grid(row=row, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def get_inputs(self):
        return (
            self.key_var.get(),
            self.name_var.get(),
            self.symbol_var.get(),
            self.user1_var.get(),
            self.plural_var.get(),
            self.desc_txt.get("1.0", "end").strip(),
        )

    def on_generate(self):
        try:
            snippet = make_glossary_entry(*self.get_inputs())
            self.preview_txt.delete("1.0", "end")
            self.preview_txt.insert("1.0", snippet)
            self.status_var.set("Generated LaTeX snippet.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error: " + str(e))

    def on_copy(self):
        text = self.preview_txt.get("1.0", "end").strip()
        if not text:
            self.on_generate()
            text = self.preview_txt.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_var.set("Snippet copied to clipboard.")
        else:
            self.status_var.set("Nothing to copy. Generate first.")

    def on_append_file(self):
        text = self.preview_txt.get("1.0", "end").strip()
        if not text:
            self.on_generate()
            text = self.preview_txt.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "Nothing to append. Generate first.")
            return
        path = filedialog.asksaveasfilename(
            title="Append to .tex file",
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
        )
        if path:
            try:
                with open(path, "a", encoding="utf-8") as f:
                    f.write("\n" + text + "\n")
                self.status_var.set(f"Appended to: {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to write file:\n{e}")

    def on_clear(self):
        self.key_var.set("")
        self.name_var.set("")
        self.symbol_var.set("")
        self.user1_var.set("")
        self.plural_var.set("")
        self.desc_txt.delete("1.0", "end")
        self.preview_txt.delete("1.0", "end")
        self.status_var.set("Cleared.")

if __name__ == "__main__":
    app = GlossaryEntryApp()
    app.mainloop()
