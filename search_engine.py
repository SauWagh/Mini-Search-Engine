import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

from PIL import Image, ImageTk
from tkinterweb import HtmlFrame

API_KEY = 'AIzaSyC4wgwhuLiX4VyhPSmRsYwHBeDlEIvjLeY'
CSE_ID  = 'b469505cfd8c74861'

def search_google():
    query = entry.get().strip()
    result.delete(1.0, tk.END)

    if not query:
        messagebox.showwarning("Warning", "Enter a search")
        return

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": f"site:youtube.com {query}"
    }

    data = requests.get(url, params=params).json()

    if "items" not in data:
        result.insert(tk.END, "No results found")
        return

    for item in data["items"][:5]:
        title = item["title"]
        link = item["link"]
        snippet = item["snippet"]

        result.insert(tk.END, title + "\n", "title")
        start = result.index(tk.END)
        result.insert(tk.END, link + "\n", "link")
        end = result.index(tk.END)

        result.tag_add(link, start, end)
        result.tag_bind(
            link,
            "<Button-1>",
            lambda e, url=link: webbrowser.open(url)
        )

        result.insert(tk.END, snippet + "\n\n")

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Search Engine")
root.geometry("700x500")

tk.Label(root, text="Search Engine", font=("Arial", 16)).pack(pady=10)

entry = tk.Entry(root, width=50, font=("Arial", 14))
entry.pack(pady=5)

tk.Button(root, text="Search", font=("Arial", 12), command=search_google).pack(pady=5)

result = tk.Text(root, wrap="word", font=("Arial", 11))
result.pack(expand=True, fill="both", padx=10, pady=10)

result.tag_config("title", font=("Arial", 12, "bold"))
result.tag_config("link", foreground="blue", underline=True)

root.mainloop()

# for Images

root = tk.Tk()
root.geometry("600x400")

panel = tk.Label(root)
panel.pack(pady=20)

img = Image.open('thumbnail.jpg')
img = img.resize((320,100))
photo = ImageTk.PhotoImage(img)

panel.config(image=photo)
panel.image = photo

root. mainloop()

# for Video

root = tk.Tk()
root.geometry("800x600")

frame = HtmlFrame(root)
frame.pack(fill="both", expand=True)

frame.load_html("""
<iframe width="100%" height="100%"
src="https://www.youtube.com/embed/VIDEO_ID"
frameborder="0" allowfullscreen></iframe>
""")

root.mainloop()