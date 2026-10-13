
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, StringVar  # برای باز کردن پنجره‌های انتخاب فایل استفاده میشه


original_image=None #آرایه عکس اولیه
edited_image=None # آرایه ی فیلترهای قبلی تمام شده
preview_image=None #  عکسی که فیلتر روش اعمال شده ولی تایید نشده
displayed_image_label=None #لیبل نمایش تصویر در صفحه اصلی
comper_label:dict[str,tk.Label|None]={"image_label_original":None,
              "image_label_edited":None,
              "image_title_original":None,
              "image_title_edited":None,
              "image_frame_original":None,
              "image_frame_edited":None}        #لیبل‌های نمایش تصاویر در حالت مقایسه

filters_visible=False # قالب فیلتر ها خاموشه

FILTERS_LIST=["Gaussian Blur","Median Blur","Blur","Bilateral","Sharpen","Flip","Rotate","Gaussian Noise"]

def create_image_label(image,Frame,width,height):
    f"""
عکس را به فرمتی تبدیل می‌کند که تیک اینتر بتواند نمایش دهد.
یک لیبل می‌سازد و عکس را داخل آن قرار می‌دهد.
خودِ لیبل را برمی‌گرداند  
  :param image: عکس اولیه یا آپدیت شده
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)  # با استفاده از آؤایه های ساخته شده توسط cv2 یک تصویر ایجاد میکند.
    image.thumbnail((width,height))  # نسبت طول و عرض اصلی عکس را حفظ کن
    image_tkv = ImageTk.PhotoImage(image)  # عکس را به فرمتی تبدیل کن که tk بتواند آن را نمایش دهد.
    image_label  = tk.Label(Frame, image=image_tkv, width=width, height=height) # یک label ایجاد شده برای نمایش عکس
    image_label .place(x=0, y=0)
    image_label .image = image_tkv  # فقط مخصوص نمایش دادن هست
    return image_label

def upload_image():
    """
پنجره انتخاب فایل, سیستم‌عامل را باز می‌کند
تصویر را میخواند و با حفظ نسبت طول و عرض عکس تغییر سایز میدهد .
عکس را داخل لیبل قرار میدهد.
    """
    global original_image
    global edited_image
    global displayed_image_label
    global preview_image

    if displayed_image_label is not None:
        displayed_image_label.destroy()
        displayed_image_label=None
    if original_image is not None:
        messagebox.showerror("Image Loading Error","Unable to load the image.")
    file_path = filedialog.askopenfilename( #از کاربر بخواه یک فایل را برای باز کردن انتخاب کند.
        title="Select an Image",#عنوان پنجره انتخاب فایل
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]) #اسم نمایشی و فایل ها با چه پسوندهایی
    if file_path:
        original_image=cv2.imread(file_path)
        edited_image=original_image.copy()
        preview_image=edited_image.copy()
        displayed_image_label=create_image_label(edited_image,image_frame,700,500)

def compare_images(click_for_upload):
    """
نمایش دو تصویرکنار یک دیگر
original , updated
    """
    global displayed_image_label  # بخشی که لیبل داره عکس رو نمایش میده
    global Display_Mode
    if displayed_image_label is not None:
        click_for_upload.place_forget()# پنهان کردن link upload
        Button_optioncompareimage.place_forget() #پنهان کلید compare
        displayed_image_label.destroy() # پاک کن عکس و لیبلش
        displayed_image_label=None
        Display_Mode="second_page"
        create_back_button()
    else:
        messagebox.showwarning("No Image Selected","please Upload an Image 62")
        return
    # ایجاد دوتا فریم روی فریم اولیه مخصوص عکس برای دوتا عکس قبل و بعد
    comper_label["image_frame_original"]=tk.Frame(image_frame,bg="#30343B",width=350,height=450)
    comper_label["image_frame_original"].place(x=0,y=20)
    comper_label["image_frame_edited"]=tk.Frame(image_frame,bg="#30343B",width=350,height=450)
    comper_label["image_frame_edited"].place(x=350,y=20)
    # title هر image
    comper_label["image_title_original"]=tk.Label(image_frame,text="Original Image",fg="#FFFFFF",bg="#30343B")
    comper_label["image_title_original"].place(x=0,y=0)
    comper_label["image_title_edited"]=tk.Label(image_frame,text="Edited Image",fg="#FFFFFF",bg="#30343B")
    comper_label["image_title_edited"].place(x=350,y=0)

    # قرار دادن عکس ها داخل  frame
    if original_image is not None and edited_image is not None :
        comper_label["image_label_original"]=create_image_label(original_image, comper_label.get("image_frame_original"), 340, 450)
        comper_label["image_label_edited"]=create_image_label(edited_image, comper_label.get("image_frame_edited"), 350, 450)
    else:
        messagebox.showwarning("Error","Some Thing Wrong 80")
        return

def show_main_view():
    """
باز گشت به صفحه ی اول و نمایش عکس آپدیت شده
    """
    global Button_backtoupdatedimage
    Button_backtoupdatedimage.destroy()
    for name,widget in comper_label.items():
        if widget is not None:
            widget.destroy()
            comper_label[name]=None
    global displayed_image_label
    global Display_Mode
    Display_Mode="main_page"
    if edited_image is not None:
        displayed_image_label=create_image_label(edited_image,image_frame,700,500)
    Button_optioncompareimage.place(x=30,y=70)

def create_back_button():
    """
ایجاد لیبل بازگشت به صفحه ی اولیه
و در صورت کلیک کردن این لیبل اطلاعات صفحه تغییر میکند.
    """
    global Button_backtoupdatedimage
    Button_backtoupdatedimage=create_action_label(root,"back to Edited Image","181A1F","FFFFFF",30,70)
    Button_backtoupdatedimage.bind("<Button-1>",lambda event: show_main_view())


def save_image():
    """
پنجره‌ای باز می‌کند تا کاربر اسم و محل ذخیره را انتخاب کند و در نهایت مسیر فایل را برمی‌گرداند.
 و بعد مسیر انتخاب شده به (cv2) داده میشود برای ذخیره
    """
    try:
        filephath=filedialog.asksaveasfilename(# لوکیشن و اسمی که میخوایی عکس رو ذخیره کنی رو انتخاب کن
            defaultextension=".jpg",#یعنی اگر کاربر پسوندی وارد نکرد، به صورت پیش‌فرض .jpg قرار بده.
            filetypes=[("Image JPG","*.jpg"),("Image PNG","*.png")]#کاربر چه نوع فایل‌هایی بتواند برای ذخیره انتخاب کند.
    )
        cv2.imwrite(filephath,edited_image)
    except Exception as e:
        print(f"Error Saving Image : {e}")

def create_action_label(Frameimage,text,bg,fg,x,y):
    """
نمایش کلید برای بخش عکس اصلی و عکس آپدیت شده
    """
    Button_option=tk.Label(Frameimage,text=f"{f'{text}':^25}",bg=f"#{bg}",fg=f"#{fg}",font=("Arial",12),cursor="hand2")
    Button_option.place(x=x,y=y)
    return Button_option

def remove_image():
    global original_image,edited_image,preview_image,displayed_image_label
    original_image=None
    edited_image=None
    preview_image=None
    if Display_Mode=="second_page" :
        show_main_view()
    else:
        if displayed_image_label is not None:
            displayed_image_label.destroy()
            displayed_image_label=None
    click_for_upload.place(x=300, y=250)


#ایجاد صفحه
root=tk.Tk()
root.title("Mini Image Editor")
root.geometry("1000x700")
root.configure(background="#181A1F")

#عنوان
title = tk.Label(root, text="Image Filter App",font=("Arial",10),bg="#181A1F",fg="#F5F5F5") # ایجاد یک متن روی تصویر
title.pack(anchor="center")# نمایش متن روی تصویر

#کادر نمایش عکس

image_frame=tk.Frame(root,bg="#30343B",width=700,height=500)
image_frame.place(x=50,y=150)
Display_Mode = "main_page"
#متن داخل کادر
click_for_upload=tk.Label(image_frame,text="Click to Upload an Image",font=("Arial",10),background="#30343B",foreground="#F5F5F5",
cursor="hand2")
click_for_upload.place(x=300,y=250)
#اتصال متن به تابع برای آپلود عکس
click_for_upload.bind("<Button-1>",lambda event:upload_image()) # کلیک چپ و اجرای تابع

# کلید Save Image
Button_option_saveimage=create_action_label(root,"Save Image","181A1F","FFFFFF",30,30)
Button_option_saveimage.bind("<Button-1>",lambda event:save_image())#ذخیره کردن عکس

# جدا کردن با ___
create_action_label(root,"-"*35,"181A1F","FFFFFF",30,50)
#کلید نمایش دادن قبل و بعد تصویر
Button_optioncompareimage=create_action_label(root,"Compare Images","181A1F","FFFFFF",30,70)
Button_optioncompareimage.bind("<Button-1>", lambda event: compare_images(click_for_upload))
#جداکردن با ___
create_action_label(root,"-"*35,"181A1F","FFFFFF",30,90)
#نمایش کلید Change Image
Button_optionChangeImage=create_action_label(root,"Remove Image","181A1F","FFFFFF",30,110)
Button_optionChangeImage.bind("<Button-1>",lambda event: remove_image())


#ایجاد بخش ایتم های فیلتر

#ایجاد کردن کلید فیلتر
def toggle_filters():
    """
     باز و بسته کردن پنل فیلترها
    """
    global filters_visible
    if not filters_visible:
        Filters_list_Frame.place(x=778, y=100)
        filters_visible=True
    else:
        Filters_list_Frame.place_forget()
        filters_visible=False

def BackToFilterFrame():
    """
تغییر حالت کلید فیلترها
    """
    show_filtered_image(edited_image)
    Filter_Frame.place_forget()
    Filters_list_Frame.place(x=778, y=100)
    Button_Filters.configure(text="Filters",command=toggle_filters)

def Change_Button_Name():
    """
تغییر کلید از فیلتر به کلیدی برای نمایش صفحه ی قبل
    """
    Button_Filters.configure(text="Back to Filters",command=BackToFilterFrame)

def Show_filter_plane():
    """
اگر بخش نمایش اطلاعات یک فیلتر فعال شد بیا قالب فیلترها رو پنهان کن و یک قالب جدیذد بساز
و پاک کردن اطلاعات قالب قبلی فیلتر
    """
    # پاک کردن محتوای قبلی
    for widget in Filter_Frame.winfo_children():
        widget.destroy()
    Filter_Frame.place(x=778, y=100)
    Filters_list_Frame.place_forget()

def filter_name_label(text,bg,fg,x,y,Frame,text_size):
    """
قرار دادن نام فیلتر ها در قالب های مورد نظر
    :param Frame: قالب مورد نیازمون
    :param text: متن ی که روی قالب قرار میگیره
    :param bg: رنگ پس زمینه
    :param fg: رنگ متن
    :param x: محور ایکس
    :param y: محور ایگرگ
    :return: بازگرداندن لیبل
    """
    label=tk.Label(Frame, text=text, bg=bg, fg=fg, cursor="hand2", font=("Arial", text_size))
    label.place(x=x, y=y)
    return label

def preview_image_to_edited_image(filter_name):
    """
     تاییید عکس ادیت شده و اپدیت
     خاموش کردن ویجت ها
    :param filter_name:
    """
    global edited_image
    global preview_image
    edited_image=preview_image
    preview_image=None
    reset_Filters(filter_name)

def reset_Filters(filter_name):
    """
    پاک کردن ویجت های روی فریم
    صفر کردن فیلتر ها روی عکس و ویجت ها
    :param filter_name:اسم فیلتر
    """
    global preview_image #  عکسی که فیلتر روش اعمال شده ولی تایید نشده
    for widget in Filter_Frame.winfo_children():
        widget.destroy()
    select_filter(filter_name) #ایجاد فیلتر
    show_filtered_image(edited_image)

def show_filtered_image(filtered_image):
    """
    عکس رو دریافت و فریم رو پیدا
    و سپس عکس رو برای نمایش به تابع 'ایجاد لیبل عکس' میدهد.
    :param filtered_image: عکس
    """
    global edited_image
    global preview_image #  عکسی که فیلتر روش اعمال شده ولی تایید نشده
    global displayed_image_label
    if displayed_image_label is not None:
        displayed_image_label.destroy()
        displayed_image_label=None
    if Display_Mode=="main_page":
        targetframe=image_frame
        width=700
        height=500
    else:
        targetframe=comper_label.get("image_frame_edited")
        width=350
        height=450
    displayed_image_label=create_image_label(filtered_image,targetframe,width,height)
    preview_image=filtered_image

def select_filter(filter_name):
    """
اجرای توابعی که بعد از انتخاب یک فیلتر لازمه مثلا تغییر قالب یا پاک کردن اطلاعات قالب قبلی
    :param filter_name: نام فیلتر انتخاب شده
    """
    Change_Button_Name()
    Show_filter_plane()
    filter_name_label(filter_name, "#24272D", "#FFFFFF",0, 0,Filter_Frame,12)
    create_filter_widgets(filter_name)
    #کلید پاک کردن دیتای ویجت ها
    clear = tk.Button(Filter_Frame, text="Clear", bg="#24272D", fg="#FFFFFF", font=("Arial", 12), width=10, height=1,
    command=lambda :reset_Filters(filter_name))
    #کلید ثبت ادیت روی عکس
    apply=tk.Button(Filter_Frame,text="Apply Filter",bg="#24272D",fg="#FFFFFF", font=("Arial", 12), width=10, height=1
    ,command=lambda:preview_image_to_edited_image(filter_name))
    clear.place(x=0, y=300)
    apply.place(x=100, y=300)

def apply_gaussian_blur(Ksize_value=1,sigma_value=0):
    """
بلر کردن به روش گاوسی
میانگین میگیره از پیکسل های اطراف + وزن هر پیکس تاثییر گذاره
    :param Ksize_value:اندازه ی پیکسل های تاثییر گذار اطرافا
    :param sigma_value: وزن هر پیکسل - 0 یعنی خود سیستم تصمیم بگیره
    """
    gaussianblur=cv2.GaussianBlur(edited_image,(Ksize_value,Ksize_value),sigmaX=sigma_value)
    show_filtered_image(gaussianblur)
def apply_median_blur(Ksize_value=1):
    """
بلر کردن به روش میانه گیری
    :param Ksize_value: اندازه ی پیکسل های تاثییر گذار اطراف
    """
    medianblure=cv2.medianBlur(edited_image,Ksize_value)
    show_filtered_image(medianblure)
def apply_box_blur(Ksize_value=1):
    """
بلر کردن ساده
    :param Ksize_value: اندازه ی پیکسل های تاثییر گذار اطراف
    """
    blur=cv2.blur(edited_image,(Ksize_value,Ksize_value))
    show_filtered_image(blur)
def apply_bilateral_filter(Ksize_value=1,sigmacolor=0,sigmaspace=0):
    """
بلر کردن با روش میانگین گیری
وزن هر پیکسل ورنگ هر پیکسل تاثییر گذاره

    :param Ksize_value: اندازه ی پیکسل های تاثییر گذار اطراف
    :param sigmacolor: اختلاف تاثییر گذار در وزن رنگ
    :param sigmaspace: اختلاف تاثییر گذار در وزن فاصله
    """
    bilateralImage=cv2.bilateralFilter(edited_image,Ksize_value,sigmaColor=sigmacolor,sigmaSpace=sigmaspace)
    show_filtered_image(bilateralImage)
def apply_sharpen(strength=5):
    """
برای تیز کردن لبه های عکس
    :param strength:
    """
    kernel=np.array([[0,(1-strength)//4,0],[(1-strength)//4,strength,(1-strength)//4],[0,(1-strength)//4,0]])
    sharpenImage=cv2.filter2D(edited_image,-1,kernel)
    show_filtered_image(sharpenImage)
def apply_flip(flipcode):
    """
چرخش عکس به صورت عمودی و افقی
    :param flipcode: کد چرخش
    """
    flipImage=cv2.flip(preview_image,int(flipcode))
    show_filtered_image(flipImage)
def apply_rotate(angle):
    """
ضرایب مربوط به چرخش
عکس رو به درجه های پیشنهادی میچرخانیم
    :param angle:درجه
    """
    h,w=edited_image.shape[:2]
    center=(w//2,h//2)
    rotate_matrix=cv2.getRotationMatrix2D(center,angle,1)# یک ماتریس ساخته شد برای چرخاندن عکس
    matrix_cos=abs(rotate_matrix[0,0]) # ضریب کسینوس رو میده
    matrix_sin=abs(rotate_matrix[0,1])# ضریب سینوس رو میده

    new_w=int((w*matrix_cos)+(h*matrix_sin))
    new_h=int((h*matrix_cos)+(w*matrix_sin))

    rotate_matrix[0,2]+=(new_w/2)-center[0] # تغییر مرکز عکس
    rotate_matrix[1,2]+=(new_h/2)-center[1]

    rotated_image=cv2.warpAffine(edited_image,rotate_matrix,(new_w,new_h))
    show_filtered_image(rotated_image)

def apply_gaussian_noise(deviation):
    """
ایجاد نویز روی عکس
    param deviation: انحراف معیار
    """
    Noise=np.random.normal(0,deviation,edited_image.shape).astype(np.uint8) #به تعداد پیکس های عکس - به صورت نرمال ارایه ای بساز با انحراف معیار مشخص شده - میانگین 0 در نظر گرفته شده
    new_image=cv2.add(edited_image,Noise)
    show_filtered_image(new_image)

def create_filter_widgets(filter_name):
    """
ایجاد ویجت های اختصاصی برای هر فیلتر
    """
    if filter_name =="Gaussian Blur":
        # اسکرول سایز
        scale_ksize = tk.Scale(Filter_Frame, orient="horizontal", from_=1, to=21, resolution=2, troughcolor="#24272D",
        activebackground="#FFFFFF",highlightthickness=0, label="Ksize", fg="#FFFFFF", bg="#24272D", relief="flat", length=190,
        width=5, sliderlength=50, command=lambda value: apply_gaussian_blur(int(value),int(spinbox.get())))
        # ایجاد لیبل سیگما
        entery_label = tk.Label(Filter_Frame, text="Sigma X:", width=7, height=1, bg="#24272D", fg="#FFFFFF")
        # کادر برای گرفتن مقدار سیگما
        spinbox = tk.Spinbox(Filter_Frame,from_=0,to=100,width=5,font=("Arial",11),command=lambda: apply_gaussian_blur(int(scale_ksize.get()),int(spinbox.get())))
        scale_ksize.place(x=0, y=40)
        entery_label.place(x=0, y=110)
        spinbox.place(x=60, y=110)

    elif filter_name == "Median Blur":
        scale_ksize=tk.Scale(Filter_Frame,label="Ksize",orient="horizontal",from_=1,to=21,resolution=2,troughcolor="#24272D",
        fg="#FFFFFF", bg="#24272D",highlightthickness=0,relief="flat",activebackground="#FFFFFF",length=190,sliderlength=50,width=5
        ,command=lambda value:apply_median_blur(int(value)))
        scale_ksize.place(x=0, y=40)

    elif filter_name=="Blur":
        scale_ksize=tk.Scale(Filter_Frame,label="Ksize",orient="horizontal",from_=1,to=21,resolution=2,troughcolor="#24272D",
        fg="#FFFFFF",bg="#24272D",length=190,relief="flat",highlightthickness=0,sliderlength=50,activebackground="#FFFFFF",width=5,command=lambda value:apply_box_blur(int(value)))
        scale_ksize.place(x=0, y=40)

    elif filter_name =="Bilateral":
        # حساس به رنگ - حساس به وزن - اندازه ی فضای اطراف برای تاثیر
        label_sigmaspace = tk.Label(Filter_Frame, text="Sigma Space :", width=11, height=1, bg="#24272D", fg="#FFFFFF")
        label_sigmacolor = tk.Label(Filter_Frame, text="Sigma Color :", width=11, height=1, bg="#24272D", fg="#FFFFFF")

        scale_diameter = tk.Scale(Filter_Frame, label="Ksize", orient="horizontal", from_=1, to=21, resolution=2,troughcolor="#24272D",
        fg="#FFFFFF", bg="#24272D", length=190, relief="flat", highlightthickness=0,
        sliderlength=50, activebackground="#FFFFFF", width=5,command=lambda value:apply_bilateral_filter(int(value),int(scale_sigmacolor.get()),int(scale_sigmaspace.get())))
        scale_diameter.place(x=0, y=40)
        scale_sigmaspace=tk.Spinbox(Filter_Frame,from_=0,to=200,state="readonly",width=5,increment=5,font=("Arial",11),command=lambda :apply_bilateral_filter(int(scale_diameter.get()),int(scale_sigmacolor.get()),int(scale_sigmaspace.get())))
        scale_sigmacolor=tk.Spinbox(Filter_Frame,from_=0,to=150,state="readonly",width=5,increment=5,font=("Arial",11),command=lambda:apply_bilateral_filter(int(scale_diameter.get()),int(scale_sigmacolor.get()),int(scale_sigmaspace.get())))

        scale_diameter.place(x=0, y=40)
        label_sigmaspace.place(x=0, y=130)
        label_sigmacolor.place(x=90, y=130)
        scale_sigmaspace.place(x=20, y=160)
        scale_sigmacolor.place(x=110, y=160)

    elif filter_name=="Sharpen":
        strength=tk.Scale(Filter_Frame,label="Strength", orient="horizontal", from_=1, to=21, resolution=2,troughcolor="#24272D",
        fg="#FFFFFF", bg="#24272D", length=190, relief="flat", highlightthickness=0,font=("Arial",10),
        sliderlength=50, activebackground="#FFFFFF", width=5,command=lambda value:apply_sharpen(int(value)))
        strength.place(x=0, y=40)

    elif filter_name=="Flip":
        flip_code =tk.IntVar(value=1)
        flipcode_h=tk.Radiobutton(Filter_Frame,text="Horizontal",bg="#24272D",fg="#FFFFFF" ,selectcolor="#30343B",value=1,command=lambda: apply_flip(1))
        flipcode_h.place(x=0, y=100)
        flipcode_v=tk.Radiobutton(Filter_Frame,text="Vertical",bg="#24272D",fg="#FFFFFF",selectcolor="#30343B",value=0,command=lambda: apply_flip(0))
        flipcode_v.place(x=0, y=130)
        flipcode_B=tk.Radiobutton(Filter_Frame,text="Both",bg="#24272D",fg="#FFFFFF",selectcolor="#30343B",value=-1,command=lambda: apply_flip(-1))
        flipcode_B.place(x=0, y=160)

    elif filter_name=="Rotate":
        angle=tk.Scale(Filter_Frame,label="angle", orient="horizontal", from_=-180, to=180, resolution=1,troughcolor="#24272D",
        fg="#FFFFFF", bg="#24272D", length=190, relief="flat", highlightthickness=0,font=("Arial",10),
        sliderlength=50, activebackground="#FFFFFF", width=5,command=lambda value:apply_rotate(int(value)))
        angle.place(x=0,y=40)

    elif filter_name=="Gaussian Noise":
        label_type_Noise=tk.Label(Filter_Frame,text="Noise Type",font=("Arial",9),bg="#24272D",fg="#FFFFFF").place(x=0,y=40)
        Noise_type=ttk.Combobox(Filter_Frame,width=15,state="readonly",values=["Gaussian"])
        Noise_type.current(0)
        Noise_type.place(x=2,y=60)
        label_scale=tk.Label(Filter_Frame,text="Deviation",bg="#24272D",font=("Arial",10),fg="#FFFFFF",highlightthickness=0).place(x=0,y=107)
        standard_deviation=tk.Scale(Filter_Frame,bg="#24272D",fg="#FFFFFF",from_=0,to=50,resolution=5,length=190
        ,highlightbackground="#24272D",sliderlength=50,highlightthickness=0,width=5,orient="horizontal",troughcolor="#24272D",command=lambda value:apply_gaussian_noise(int(value)))
        standard_deviation.place(x=0,y=130)

#فریم پنل فیلترها
Filters_list_Frame = tk.Frame(root, bg="#24272D", width=200, height=565)
#فریم پنل هر فیلتر
Filter_Frame = tk.Frame(root, bg="#24272D", width=200, height=565)

#کلید فیلتر
Button_Filters = tk.Button(root,text="Filters",bg="#3A3F48",fg="#FFFFFF",
width=22,height=2,font=("Arial", 12),cursor="hand2",command=toggle_filters)
Button_Filters.place(x=775,y=50)

for i,filter in enumerate(FILTERS_LIST):
    y_filters_panel=i*30
    label=filter_name_label(filter,"#24272D","#FFFFFF",0,y_filters_panel,Filters_list_Frame,10)
    label.bind("<Button-1>",lambda event,filter_name=filter:(select_filter(filter_name)))


root.mainloop()


