# jpg_to_gif_or_mp4_converter
jpg 의 이미지를 gif 나 mp4 영상으로 변환할수 있게하는 .py 코드입니다. (py ver 3.14)
</br>
</br>

### 이 프로그램은 python 3.14 버젼에서 작성되었습니다.  
따라서 그보다 낮은 버젼에선 정확하게 작동하지 아니할 수 있으며 이에 대한 대처는 어려운점 양해 부탁드립니다.

- - -

이 프로그램은 다음 제3자 Python 라이브러리를 사용합니다.

- Pillow — JPG 이미지를 GIF로 변환
- OpenCV (`opencv-python`) — JPG 이미지를 MP4로 변환
- NumPy — OpenCV 이미지 처리

- - -

사용하시기 전에 

```python
pip install pillow opencv-python numpy

pip install pillow

pip install opencv-python
```
 다음 라이브러리들을 설치해 주셔야 사용이 가능합니다.
 
</br>
</br>

- - -

```python
FPS = 2

GIF_FRAME_DURATION_MS = 500
````

이 부분을 수정하여서 바뀐 mp4 나 gif 의 jpg 가 바뀌는 속도를 지정할 수 있습니다.

- - -
</br>
</br>

이 .py 프로그램을 실행 시키신 뒤 <code>.jpg</code> 파일이 위치한 경로로 이동하십시오.  
</br>
그 다음 <code>.jpg</code> 파일을 고른 후 <code>.gif / .mp4</code> 중 원하는 형식을 고르십시오.    
</br>
<code>.gif / .mp4</code> 파일이 출력될 폴더를 고르면 그 폴더에 선택한 파일이 출력됩니다.  

</br>
아래에 자세한 사용방법 영상이 첨부 되어 있습니다.
</br>
</br>

https://github.com/user-attachments/assets/a4021817-6f87-4afe-96cc-9136f6f751dc



