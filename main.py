import cv2, time, numpy as np 
import mediapipe as mp

H = mp.solutions.hands
TIP = H.HandLandmark
ids = {
    "THUMB_TIP": TIP.THUMB_TIP,
    "INDEX_FINGER_TIP": TIP.INDEX_FINGER_TIP,
    "MIDDLE_FINGER_TIP": TIP.MIDDLE_FINGER_TIP,
    "RING_FINGER_TIP": TIP.RING_FINGER_TIP,
    "PINKY_TIP": TIP.PINKY_TIP
}
hands = H.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils
pairs = {"middle":("SEPIA","NEGATIVE"), "ring":("BLUR","GLITCH"), "pinky":("EDGE","CARTOON")}
st = {k:0 for k in pairs}; cur = "SEPIA"
DEB, CAP, TT, TP = 0.6, 1.2, 30, 20
la = lc = 0; pich_on = False 
MAIN, POP = "Gesture-Controlled Photo App", "Captured (ESC \ Close tooo resume)"
paused  = False; freeze = None
SEPIA = np.array([[0.272, 0.534, 0.131],
                  [0.349, 0.686, 0.168],[0.393, 0.769, 0.189]])
def apply(img,t):
    if t=="SEPIA": return cv2.transform(img,SEPIA)
    if t=="NEGATIVE": return cv2.bitwise_not(img)
    if t=="BLUR": return cv2.GaussianBlur(img,(15,15),0)
    if t=="GLITCH":
        b,g,r = cv2.split(img); b = np.roll(b,5,axis=1); g = np.roll(g,-5,axis=1)
        return cv2.merge((b,g,r))
    if t=="EDGE": return cv2.Canny(img,100,200)
    if t=="CARTOON":
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,5)
        edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY,9,9)
        color = cv2.bilateralFilter(img,9,250,250)
        return cv2.bitwise_and(color,color,mask=edges)

cap = cv2.VideoCapture(0)
if not cap.isOpened(): raise IOError("Cannot open webcam"); exit()
cv2.namedWindow(MAIN, cv2.WINDOW_NORMAL)
while True:
    if paused:
        cv2.imshow(MAIN,freeze)
        k = cv2.waitKey(50) & 0xFF
        if k == ord('q'): break
        if k == 27:
            paused = False; pinch_on = False
            try: cv2.destroyWindow(POP)
            except: pass
        continue
    try:
        if cv2.getWindowProperty(MAIN, cv2.WND_PROP_VISIBLE) <= 0: paused = False; pinch_on = False
    except cv2.error:
        paused = False; pinch_on = False
        continue
 

        