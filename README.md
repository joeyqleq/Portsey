# Portsey v2 🚀

Portsey is a polished, modern Python script that shows all open ports on your machine — like `netstat -tuln` — but with a much richer output. It ties each open port to its related process, binary, and Docker container (if running), thanks to the power of `lsof` and Python. 

No more memorizing complex terminal one-liners — Portsey gives you all the important info in one clean, emoji-enhanced table.

## 🧠 Why I Built This

I couldn’t find a simple, complete tool to audit local ports across multiple environments. Everything online was either:
- Too complex (chaining `lsof`, `netstat`, `ss`, `awk`, etc.),
- Or too limited (missing Docker support or process names).

So I learned Python and built one myself. This is version 2 — leaner, cleaner, more portable.

---

## 📦 Requirements

- Python 3.6+ (Python 3.13+ recommended)
- `lsof` (preinstalled on macOS/Linux)
- `pip install` the following modules:

```bash
pip install -r requirements.txt
```

### `requirements.txt` contents:
```
rich
pyfiglet
```

---

## 🛠️ Installation

It's recommended to run Portsey in a Python virtual environment:

```bash
python3 -m venv portsey-env
source portsey-env/bin/activate
pip install -r requirements.txt
```

Then run the script:

```bash
python3 portsey.py
```
---

## 🧪 Features

- Shows active ports and the binaries behind them
- Maps Docker containers to their exposed ports
- Auto-labels known apps (like Chrome, Docker, VS Code) with smart glyphs
- Handles systems where Docker is installed but not running
- Friendly error messages

---

## 🧠 Platform Support

| OS         | Status        |
|------------|---------------|
| macOS      | ✅ Supported  |
| Linux      | ✅ Supported  |
| Windows    | ❌ Not supported (yet) |

---

## 👀 Example Output

When you run `ports`, you’ll see something like:

```
Port   | Service     | Binary     | Glyph | Container
-----------------------------------------------------
8080   | http-alt    | python3    | 🐍    | -
5432   | postgres    | postgres   | 🐘    | my_db
3000   | dev server  | node       | 🟢    | -
```

---

## 🧼 Uninstall / Cleanup

Just delete the folder and remove the alias from your shell config file (`~/.zshrc` or `~/.bashrc`).

---

## ✍️ Author

Created with love and lots of trial-and-error by [joeyq](https://github.com/joeyqleq).

---