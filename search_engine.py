import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk
from io import BytesIO

# ---------------- LOAD ENV ----------------
load_dotenv()
API_KEY = os.getenv("ADMIN_API_KEY")
CSE_ID  = os.getenv("ADMIN_CSE_ID")

# ---------------- CLEAR RESULTS ----------------
def clear_results():
    for w in results_frame.winfo_children():
        w.destroy()
    result_text.delete(1.0, tk.END)

# ---------------- YOUTUBE SEARCH ----------------
def search_youtube():
    query = entry.get().strip()
    clear_results()

    if not query:
        messagebox.showwarning("Warning", "Enter a search")
        return

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }

    data = requests.get(url, params=params).json()

    if "error" in data:
        result_text.insert(tk.END, data["error"]["message"])
        return

    for item in data.get("items", []):
        show_video(item)

# ---------------- SHOW VIDEO ----------------
def show_video(item):
    title = item["snippet"]["title"]
    video_id = item["id"]["videoId"]
    thumb_url = item["snippet"]["thumbnails"]["medium"]["url"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    frame = tk.Frame(results_frame, pady=8)
    frame.pack(fill="x", anchor="w")

    img_data = requests.get(thumb_url).content
    img = Image.open(BytesIO(img_data)).resize((200, 120))
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(frame, image=photo, cursor="hand2")
    img_label.image = photo
    img_label.pack(side="left", padx=5)
    img_label.bind("<Button-1>", lambda e: webbrowser.open(video_url))

    text = tk.Label(
        frame, text=title,
        font=("Arial", 11, "bold"),
        wraplength=450, justify="left",
        cursor="hand2"
    )
    text.pack(anchor="w")
    text.bind("<Button-1>", lambda e: webbrowser.open(video_url))

# ---------------- WEB SEARCH ----------------
def search_web():
    query = entry.get().strip()
    clear_results()

    if not query:
        messagebox.showwarning("Warning", "Enter a search")
        return

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query
    }

    data = requests.get(url, params=params).json()

    if "error" in data:
        result_text.insert(tk.END, data["error"]["message"])
        return

    for item in data.get("items", [])[:5]:
        frame = tk.Frame(results_frame, pady=8)
        frame.pack(fill="x", anchor="w")

        title = tk.Label(
            frame, text=item["title"],
            font=("Arial", 11, "bold"),
            wraplength=650, justify="left",
            cursor="hand2"
        )
        title.pack(anchor="w")
        title.bind("<Button-1>", lambda e, url=item["link"]: webbrowser.open(url))

        link = tk.Label(
            frame, text=item["link"],
            fg="blue", cursor="hand2",
            wraplength=650
        )
        link.pack(anchor="w")
        link.bind("<Button-1>", lambda e, url=item["link"]: webbrowser.open(url))

        snippet = tk.Label(frame, text=item["snippet"], wraplength=650)
        snippet.pack(anchor="w")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Mini Search Engine")
root.geometry("800x550")

tk.Label(root, text="Search Engine", font=("Arial", 16)).pack(pady=10)

entry = tk.Entry(root, width=55, font=("Arial", 14))
entry.pack(pady=5)

tk.Button(root, text="YouTube Videos", command=search_youtube).pack(pady=2)
tk.Button(root, text="Web Search", command=search_web).pack(pady=2)

container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, command=canvas.yview)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

results_frame = scroll_frame

result_text = tk.Text(root, height=3)
result_text.pack(fill="x")

root.mainloop()
