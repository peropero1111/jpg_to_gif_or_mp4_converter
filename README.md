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
python -m pip install numpy

python -m pip install pillow

python -m pip install opencv-python
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
<img src="https://github.com/peropero1111/jpg_to_gif_or_mp4_converter/blob/main/img/2026-09-15%20182413.png?raw=true" width="450" height="450"/> 

</br>
</br>
그 다음 <code>.jpg</code> 파일을 고른 후 <code>.gif / .mp4</code> 중 원하는 형식을 고르십시오.    
</br>
</br>
<img src="https://github.com/peropero1111/jpg_to_gif_or_mp4_converter/blob/main/img/2026-09-15%20182559.png?raw=true" width="350" height="350"/><img src="https://github.com/peropero1111/jpg_to_gif_or_mp4_converter/blob/main/img/2026-09-15%20182451.png?raw=true" width="250" height="250"/> 



</br>
</br>
<code>.gif / .mp4</code> 파일이 출력될 폴더를 고르면 그 폴더에 선택한 파일이 출력됩니다.  
<br>
<br>
<img src="https://github.com/peropero1111/jpg_to_gif_or_mp4_converter/blob/main/img/2026-09-15%20183422.png?raw=true" width="450" height="450"/> 

</br>
아래에 자세한 사용방법 영상이 첨부 되어 있습니다.
</br>
</br>

https://github.com/user-attachments/assets/a4021817-6f87-4afe-96cc-9136f6f751dc

- - -

## 라이선스

이 프로젝트의 직접 작성된 소스 코드는 MIT License에 따라 배포됩니다.

자세한 내용은 [`LICENSE`](LICENSE) 파일을 참고하십시오.

이 프로젝트에서 사용하는 제3자 라이브러리에는 각각 해당 프로젝트의
별도 라이선스가 적용되며, 이 저장소의 MIT License가 해당 라이브러리
자체에 적용되는 것은 아닙니다.

- - -

면책조항

이 소프트웨어는 어떠한 종류의 명시적 또는 묵시적 보증 없이
"있는 그대로(AS IS)" 제공됩니다.

jpg_to_gif_or_mp4_converter는 여러 JPG 이미지를 GIF 또는 MP4 파일로
변환하기 위한 보조 도구입니다.

프로젝트 작성자는 다음 사항을 보장하지 않습니다.

* 모든 JPG 이미지가 정상적으로 변환되는 것
* 모든 이미지 형식, 해상도 또는 색상 형식을 지원하는 것
* 생성된 GIF 또는 MP4 파일이 모든 프로그램과 기기에서 정상적으로 재생되는 것
* 변환 과정에서 원본과 동일한 화질, 색상 또는 이미지 품질이 유지되는 것
* 프로그램이 모든 운영체제 및 Python 환경에서 동일하게 작동하는 것
* 프로그램 또는 사용 중인 제3자 라이브러리가 항상 오류 없이 작동하는 것

중요한 이미지 파일을 변환하기 전에 원본 파일의 백업을 보관하는 것을
권장합니다.

프로그램 사용 중 발생한 데이터 손실, 파일 손상, 변환 실패,
출력 파일의 호환성 문제 또는 기타 손해에 대한 책임은 저장소의
LICENSE에 규정된 범위 내에서 제한됩니다.

- - -

파일 변환 관련 안내

변환 결과는 입력 이미지의 해상도, 크기, 색상 형식, 이미지 수 및
사용 환경에 따라 달라질 수 있습니다.

MP4 또는 GIF 형식으로 변환하는 과정에서 압축 또는 인코딩으로 인해
원본 이미지와 비교하여 화질이나 색상에 차이가 발생할 수 있습니다.

생성된 파일을 중요한 작업에 사용하기 전에는 정상적으로 재생되는지
직접 확인하는 것을 권장합니다.

- - -
이 저장소에 사용된 예시 이미지는 ChatGPT의 이미지 생성 기능을 통해 제작되었습니다.
