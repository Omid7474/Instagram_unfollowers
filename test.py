import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
import os
import webbrowser
from extractJson import jsonExt
from extractHtml import htmlExt

class InstagramFollowerAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.style = Style()
        self.current_index = 0
        self.urls = []

        root.title("Instagram Follower Analysis")
        self.instruction_label = tk.Label(root, text="Choose the type of file you want to process:")
        self.instruction_label.pack(pady=10)

        self.json_button = tk.Button(root, text="JSON", command=self.process_json)
        self.json_button.pack(pady=5)

        self.html_button = tk.Button(root, text="HTML", command=self.process_html)
        self.html_button.pack(pady=5)

        self.open_urls_button = tk.Button(root, text="Open URLs", command=self.open_urls, state=tk.DISABLED)
        self.open_urls_button.pack(pady=5)

    def process_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        followers_file = filedialog.askopenfilename(initialdir=current_dir, title="Select Followers JSON File", filetypes=[("JSON files", "*.json")])
        if not followers_file:
            return
        following_file = filedialog.askopenfilename(initialdir=current_dir, title="Select Following JSON File", filetypes=[("JSON files", "*.json")])
        if not following_file:
            return

        try:
            not_following_back, not_following_back_urls = jsonExt(followers_file, following_file)
            self.display_results(not_following_back, not_following_back_urls)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing JSON files: {e}")

    def process_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        followers_html = filedialog.askopenfilename(initialdir=current_dir, title="Select Followers HTML File", filetypes=[("HTML files", "*.html")])
        if not followers_html:
            return
        following_html = filedialog.askopenfilename(initialdir=current_dir, title="Select Following HTML File", filetypes=[("HTML files", "*.html")])
        if not following_html:
            return

        try:
            not_following_back, not_following_back_urls = htmlExt(followers_html, following_html)
            self.display_results(not_following_back, not_following_back_urls)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing HTML files: {e}")

    def display_results(self, not_following_back, not_following_back_urls):
        results_window = tk.Toplevel(self.root)
        results_window.title("Results")

        not_following_back_label = tk.Label(results_window, text="Users not following back with URLs:")
        not_following_back_label.pack()

        results_listbox = tk.Listbox(results_window, width=100, height=20)
        results_listbox.pack()

        for user, url in zip(not_following_back, not_following_back_urls):
            results_listbox.insert(tk.END, f"{user} - {url}")

        self.urls = not_following_back_urls
        self.current_index = 0
        self.open_urls_button.config(state=tk.NORMAL)

    def open_urls(self):
        if not self.urls:
            return
        
        end_index = min(self.current_index + 15, len(self.urls))
        for url in self.urls[self.current_index:end_index]:
            webbrowser.open(url)
        
        self.current_index = end_index
        
        if self.current_index >= len(self.urls):
            self.open_urls_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = InstagramFollowerAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
