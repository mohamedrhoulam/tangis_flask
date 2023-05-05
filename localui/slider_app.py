import tkinter as tk

class SliderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Slider App")
        self.root.geometry("400x150")
        
        self.slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, showvalue=0)
        self.slider.pack(pady=20)
        
        self.button = tk.Button(self.root, text="Submit", command=self.submit)
        self.button.pack()
        
    def submit(self):
        value = self.slider.get()
        print("Slider value:", value)
        
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = SliderApp()
    app.run()
