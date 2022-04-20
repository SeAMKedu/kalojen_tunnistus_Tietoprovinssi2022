import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageTk
from os.path import join

class FishGui():
    """GUI kalojen tunnistukseen Tietoprovinssiin/Lasten tiedepäivään 2022.
    Käyttöliittymällä voi avata kuvia kovalevyltä tai ottaa kuvaa webkameralla
    ja käyttää opetettua neuroverkkoa tunnistamaan, onko kuvassa ahven, muikku,
    lahna vai kuore.
    """
    def __init__(self):
        """Loading the CNN and constructing the GUI
        """
        self.load_cnn()

        self.root = tk.Tk()
        gui_size = (1200, 800)
        self.root.geometry(f"{gui_size[0]}x{gui_size[1]}")
        self.img = None
        prev_width = int(gui_size[0] * 0.5)
        self.img_preview_shape = (prev_width, int(round(3/4*prev_width)))
        self.cap = None # Initalization for the possible webcam
        
        # The overall area
        self.left_frame = tk.Frame(self.root, width=int(gui_size[0]/4))
        self.right_frame = tk.Frame(self.root)
    
        # Button for running the check
        self.identify_button = tk.Button(self.left_frame, 
                                    text="Tunnista",
                                    command=self.identify)

        # Button for loading the image
        self.load_img_button = tk.Button(self.left_frame,
                                    text="Lataa kuva",
                                    command=self.load_image)

        # Choosing if the image is read from a file or from a camera
        img_src_label = tk.Label(self.left_frame, text="Kuvalähde:")
        self.radio_var = tk.IntVar()
        self.radio_var.set(1)  # initializing the choice
        self.offline_radiobutton = tk.Radiobutton(self.left_frame, text="Tallennetut kuvat", 
                                            variable=self.radio_var, value=1, command=self.stream_off)
        self.camera_radiobutton = tk.Radiobutton(self.left_frame, text="Web-kamera", 
                                            variable=self.radio_var, value=2, command=self.stream_on)
        self.img_label = tk.Label(self.root)

        # Frames
        self.left_frame.grid(row=0, column=0, padx=20, pady=20)
        self.right_frame.grid(row=0, column=1)
        self.root.grid_columnconfigure(1, minsize=self.img_preview_shape[0])

        # Packing the rest of the buttons and fields
        img_src_label.pack()
        self.offline_radiobutton.pack()
        self.camera_radiobutton.pack()
        self.load_img_button.pack()
        self.identify_button.pack()

        self.img_label.grid(row=1, column=1)
        self.root.mainloop()

    def load_cnn(self):
        # Ladataan malli ja parametrit
        model_folder = r"bs_12_epochs_100"
        self.model = tf.keras.models.load_model(model_folder)
        param_data = np.load(join(model_folder, "params.npz"))
        self.class_names = param_data["class_names"]
        self.cnn_img_height = param_data["img_height"].item()
        self.cnn_img_width = param_data["img_width"].item()

    def stream_on(self):
        """Opening a camera device when radio button is clicked
        """
        self.load_img_button["state"] = "disabled"

        # Using a webcam
        # OLETUKSENA VIDEOCAPTURELLA LAITE 0; JOS KONEESSA USEAMPIA WEB-KAMEROITA, 
        # KOKEILE MYÖS MUITA INDEKSEJÄ (1, 2, ...).
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap is None or not cap.isOpened():
            self.cap = None

            tk.messagebox.showerror("Error", "No Basler camera or webcam found!")
            self.load_img_button["state"] = "normal"
        else:
            self.cap = cap
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_preview_shape[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_preview_shape[1])
            self.show_frame()

    def stream_off(self):
        """Closing the camera device when the radio button is clicked.
        """
        self.cap.release()
        self.load_img_button["state"] = "normal"
        self.exp_time_entry["state"] = "disabled"
        self.update_exp_time_button["state"] = "disabled"
    

    def show_frame(self):
        """Showing the frame grabbed from the camera device in the GUI.
        """
        # Initializing
        frame = np.zeros(self.img_preview_shape, np.uint8)

        # If the radio button is selected, continuing capturing frames
        if self.radio_var.get() == 2:

            # Using the webcam
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            self.img = frame

            # Modifying the image to be tkinter compatible. 
            pil_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            pil_img = Image.fromarray(pil_img)
            render = ImageTk.PhotoImage(image=pil_img)

            self.img_label.configure(image=render)
            self.img_label.image = render
            self.img_label.after(10, self.show_frame)
    

    def render_image(self, image=None, max_dim=None):
        """Rendering the image so that tkinter can show it.

        Args:
            image (numpy array, optional): Image in OpenCV type. If not given,
                                            self.img will be used. Defaults to None.
            max_dim (int, optional): Maximum width of the preview image. If not given, 
                                            self.img_previw_width will be used. Defaults to None.

        Returns:
            tk image: Image in tkinter compatible format
        """
        if image is None:
            image = self.img
        if max_dim is None:
            max_dim = self.img_preview_shape[0]
        h, w, _ = image.shape
        if h > max_dim or w > max_dim:
            fx = max_dim / w
            fy = max_dim / h
            scale = min(fx, fy)

        preview_img = cv2.resize(image, None, fx=scale, fy=scale)
        pil_img = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGBA)
        pil_img = Image.fromarray(pil_img)
        render = ImageTk.PhotoImage(pil_img)
        return render

    def load_image(self):
        """Callback for pressing the Load Image button.
        """
        filename = fd.askopenfilename(initialdir=".",
                                        filetypes=[("Jpeg files", "*.jpeg"),
                                                ("Jpg files", "*.jpg"),
                                                ("Png files", "*.png"), 
                                                ("Tiff files", "*.tiff"), 
                                                ("Tif files", "*.tif")])
        if filename != "":
            img = cv2.imread(filename)
            self.img = img
            render = self.render_image()
            self.img_label.configure(image=render)
            self.img_label.image = render
    
    def update_exp_time(self):
        """Callback for pressing the Update Exposure Time button
        """
        exp_time = self.exp_time_entry.get()
        exp_time = self.read_parameter("exposure time", exp_time)
        if exp_time is not None:
            self.exp_time = exp_time
            if self.camera.IsGrabbing():
                self.camera.ExposureTimeAbs.SetValue(exp_time)
    
    @staticmethod
    def read_parameter(param_name, param, param_type="int"):
        """ Reading a chessboard parameter from the GUI and checking
        that it is in right format (integer or float)

        Args:
            param_name (string): The name of the parameter in the GUI
            param (string): The parameter read from the GUI as text
            param_type (string): Expected parameter type (Defaults to "int")

        Returns:
            int/None: The parameter as integer or None if the format is not correct
        """
        try:
            if param_type == "int":
                param = int(param)
            elif param_type == "float":
                param = float(param)
            else:
                raise ValueError(f"Incorrect type {param_type}!")
        except ValueError:
            mb.showerror("Error", f"Parameter '{param_name}' should be {param_type}!")
            return None
        else:
            if param < 0:
                mb.showerror("Error", f"Parameter '{param_name}' should be greater than zero!")
                return None
        
        return param
        

    def identify(self):
        """Callback for pressing the Tunnista button.
        """
        if self.img is None:
            mb.showerror("Virhe!", "Ei käsiteltävää kuvaa!")
        else:
            # Kuvan koko vastaamaan opetusdataa ja väriavaruus RGB:ksi
            img = cv2.resize(self.img, (self.cnn_img_width, self.cnn_img_height))
            img = img[...,::-1] # BGR -> RGB

            # Keras-maailmaan
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0) # Create a batch

            # Ennustus mallin avulla
            predictions = self.model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            predicted_class = self.class_names[np.argmax(score)] 
            
            # Näytetään tuloskuva
            result_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            plt.imshow(result_img)
            plt.title(f"Kala on {predicted_class.lower()}")
            plt.show(block=True)

        
if __name__ == "__main__":
    app = FishGui()