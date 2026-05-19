import os
import shutil
import tempfile
from tkinter import Button, Label, Radiobutton, StringVar, Tk, Toplevel, filedialog, messagebox

# GIF 변환에 필요한 Pillow 라이브러리임.
try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
    ImageOps = None

# MP4 변환에 필요한 OpenCV, NumPy 라이브러리임.
try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


# MP4 재생 속도 설정임.
# 2fps => 0.5sec
FPS = 2

# GIF 프레임 표시 시간 설정임.
# 500ms => 0.5sec
GIF_FRAME_DURATION_MS = 500


def print_progress(label, current, total):
    # 콘솔에 진행률을 같은 줄에서 갱신해 보여줌.
    percent = int((current / total) * 100)
    print(f"\r{label}: {current}/{total} ({percent}%)", end="", flush=True)

    if current == total:
        print()



def choose_output_format(root):

    # 딕셔너리를 쓰는 이유는 내부 함수 ok()에서 선택 결과를 바깥 스코프에 저장하기 위해서임.
    result = {"format": None}
    window = Toplevel(root)
    window.title("Select Output Format")
    window.resizable(False, False)

    # 이 창을 닫거나 선택하기 전까지 다른 Tkinter 창을 조작하지 못하게 함.
    window.grab_set()

    selected_format = StringVar(value="mp4")

    Label(window, text="Choose output format").pack(padx=24, pady=(18, 8))
    Radiobutton(window, text="MP4 video (.mp4)", variable=selected_format, value="mp4").pack(
        anchor="w",
        padx=24,
    )
    Radiobutton(window, text="GIF animation (.gif)", variable=selected_format, value="gif").pack(
        anchor="w",
        padx=24,
    )

    def ok():
        result["format"] = selected_format.get()
        window.destroy()

    def cancel():
        # 창의 X 버튼을 누르면 선택하지 않은 것으로 처리됨.
        window.destroy()

    Button(window, text="OK", width=12, command=ok).pack(pady=(12, 18))
    window.protocol("WM_DELETE_WINDOW", cancel)
    window.focus_force()

    root.wait_window(window)

    return result["format"]



def get_unique_output_path(output_dir, extension):
    # mp4는 결과파일이 중복되지 않도록 임시이름인 combined_1, combined_2처럼 이름을 바꿈.
    filename = f"combined.{extension}"
    base_name, file_extension = os.path.splitext(filename)
    output_file = os.path.join(output_dir, filename)
    counter = 1

    while os.path.exists(output_file):
        output_file = os.path.join(output_dir, f"{base_name}_{counter}{file_extension}")
        counter += 1

    return output_file



def get_adaptive_palette():
    # Pillow 버전에 따라 ADAPTIVE 팔레트 상수가 있는 위치가 다를 수 있어 호환 처리함.
    palette_holder = getattr(Image, "Palette", None)

    if palette_holder is not None and hasattr(palette_holder, "ADAPTIVE"):
        return palette_holder.ADAPTIVE

    return getattr(Image, "ADAPTIVE", 1)



def read_pil_image(jpg_file):
    # EXIF 회전 정보가 들어 있는 사진도 올바른 방향으로 읽어옮.
    # GIF 저장에 맞게 RGB 모드로 통일함.
    with Image.open(jpg_file) as image:
        return ImageOps.exif_transpose(image).convert("RGB")



def get_canvas_size_for_gif(jpg_files):
    # GIF는 크기가 같아야 하므로 가장 큰 너비와 높이를 찾아서 캔버스 크기로 사용함.
    max_width = 0
    max_height = 0
    total = len(jpg_files)

    for index, jpg_file in enumerate(jpg_files, start=1):
        image = read_pil_image(jpg_file)
        max_width = max(max_width, image.width)
        max_height = max(max_height, image.height)
        print_progress("Checking GIF image sizes", index, total)

    return max_width, max_height



def put_pil_image_on_canvas(image, canvas_width, canvas_height):
    # 이미지 크기가 이미 캔버스와 같으면 불필요한 복사를 하지 않고 그대로 반환함.
    if image.size == (canvas_width, canvas_height):
        return image

    # 크기가 다른 이미지는 흰 배경 캔버스 중앙에 배치함.
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    x = (canvas_width - image.width) // 2
    y = (canvas_height - image.height) // 2
    canvas.paste(image, (x, y))

    return canvas



def convert_jpgs_to_one_gif(jpg_files, gif_file):
    # 먼저 전체 이미지의 최대 크기를 구한 뒤 모든 프레임을 같은 캔버스 크기로 맞춤.
    canvas_width, canvas_height = get_canvas_size_for_gif(jpg_files)
    palette = get_adaptive_palette()
    frames = []
    total = len(jpg_files)

    for index, jpg_file in enumerate(jpg_files, start=1):
        image = read_pil_image(jpg_file)
        frame = put_pil_image_on_canvas(image, canvas_width, canvas_height)

        # GIF는 색상 수 제한이 있으므로 팔레트 모드로 변환함.
        frames.append(frame.convert("P", palette=palette))
        print_progress("Converting to GIF", index, total)

    print("Saving GIF file...")
    frames[0].save(
        gif_file,
        "GIF",
        save_all=True,              # 여러 프레임을 하나의 GIF로 저장함.
        append_images=frames[1:],   # 첫 프레임 뒤에 이어 붙일 프레임들임.
        duration=GIF_FRAME_DURATION_MS,
        loop=0,                     
        optimize=False,
    )


def read_cv2_image(jpg_file):
    # 한글 경로에서도 더 안정적으로 읽을 수 있도록 호환 처리함.
    file_bytes = np.fromfile(jpg_file, dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(f"Could not read image: {jpg_file}")

    return image


def get_canvas_size_for_mp4(jpg_files):
    # MP4도 모든 프레임 크기가 같아야 하므로 가장 큰 너비/높이를 기준으로 캔버스를 만듬.
    max_width = 0
    max_height = 0
    total = len(jpg_files)

    for index, jpg_file in enumerate(jpg_files, start=1):
        image = read_cv2_image(jpg_file)
        height, width = image.shape[:2]
        max_width = max(max_width, width)
        max_height = max(max_height, height)
        print_progress("Checking MP4 image sizes", index, total)

    # 일부 동영상 코덱은 홀수 크기 해상도를 제대로 처리하지 못할 수 있어 짝수로 맞춤.
    if max_width % 2 == 1:
        max_width += 1
    if max_height % 2 == 1:
        max_height += 1

    return max_width, max_height


def put_cv2_image_on_canvas(image, canvas_width, canvas_height):
    height, width = image.shape[:2]

    if width == canvas_width and height == canvas_height:
        return image

    # 흰색 배경 캔버스를 만들고 원본 이미지를 중앙에 배치함.
    canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
    x = (canvas_width - width) // 2
    y = (canvas_height - height) // 2
    canvas[y:y + height, x:x + width] = image

    return canvas


def convert_jpgs_to_one_mp4(jpg_files, mp4_file):
    canvas_width, canvas_height = get_canvas_size_for_mp4(jpg_files)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # 변환 도중 오류가 나도 깨진 결과 파일이 바로 생성되지 않도록 임시 파일에 먼저 저장함.
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_mp4_file = temp_file.name
    temp_file.close()

    writer = cv2.VideoWriter(temp_mp4_file, fourcc, FPS, (canvas_width, canvas_height))

    if not writer.isOpened():
        if os.path.exists(temp_mp4_file):
            os.remove(temp_mp4_file)
        raise RuntimeError("Could not create MP4 file.")

    try:
        try:
            total = len(jpg_files)

            for index, jpg_file in enumerate(jpg_files, start=1):
                image = read_cv2_image(jpg_file)
                frame = put_cv2_image_on_canvas(image, canvas_width, canvas_height)
                writer.write(frame)
                print_progress("Converting to MP4", index, total)
        finally:
            writer.release()

        # 변환이 완전히 끝난 뒤에만 최종 위치로 이동함.
        shutil.move(temp_mp4_file, mp4_file)
    except Exception:
        # 실패 시 임시 파일을 지워서 불완전한 파일이 남지 않게 함.
        if os.path.exists(temp_mp4_file):
            os.remove(temp_mp4_file)
        raise


def show_missing_library_error(output_format):
    # 사용자가 선택한 포맷에 필요한 라이브러리가 없을 때 설치 방법을 안내
    if output_format == "gif":
        messagebox.showerror(
            "Pillow required",
            "Pillow is required to convert JPG files to GIF.\n\n"
            "Please install it with this command:\n"
            "python -m pip install pillow"
        )
        return

    messagebox.showerror(
        "OpenCV required",
        "OpenCV is required to convert JPG files to MP4.\n\n"
        "Please install it with this command:\n"
        "python -m pip install opencv-python"
    )


def has_required_library(output_format):
    # 선택한 출력 포맷에 필요한 라이브러리가 import 되었는지 확인
    if output_format == "gif":
        return Image is not None and ImageOps is not None

    return cv2 is not None and np is not None


def convert_files(jpg_files, output_dir, output_format):
    # 출력 파일 경로를 정하고 선택한 포맷에 맞는 변환 함수를 호출
    output_file = get_unique_output_path(output_dir, output_format)

    if output_format == "gif":
        convert_jpgs_to_one_gif(jpg_files, output_file)
    else:
        convert_jpgs_to_one_mp4(jpg_files, output_file)

    return output_file


def main():
    root = Tk()
    root.withdraw()

    jpg_files = filedialog.askopenfilenames(
        title="Select JPG Files",
        filetypes=[
            ("JPG files", "*.jpg *.jpeg"),
            ("All files", "*.*"),
        ],
    )

    if not jpg_files:
        print("No files selected.")
        root.destroy()
        return

    output_format = choose_output_format(root)

    if output_format is None:
        print("No output format selected.")
        root.destroy()
        return

    if not has_required_library(output_format):
        show_missing_library_error(output_format)
        root.destroy()
        return

    output_dir = filedialog.askdirectory(title="Select Output Folder")

    if not output_dir:
        print("No output folder selected.")
        root.destroy()
        return

    try:
        output_file = convert_files(jpg_files, output_dir, output_format)
    except Exception as error:
        # 예외 msg 박스는 출력
        messagebox.showerror("Error", str(error))
        root.destroy()
        return

    messagebox.showinfo(
        "Done",
        f"Combined {len(jpg_files)} file(s) into one {output_format.upper()}."
    )
    print(f"Converted {len(jpg_files)} file(s) -> {output_file}")
    root.destroy()


if __name__ == "__main__":
    main()
