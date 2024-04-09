import cv2
from deepface import DeepFace

img=cv2.imread("chris.png")

res=DeepFace.analyze(img, actions=("gender","age","emotion"))

print("Gender:",res[0]["dominant_gender"] )
print("Age:",res[0]["age"])
print("Emotion:", res[0]["dominant_emotion"])