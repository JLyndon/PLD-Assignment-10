import cv2 as CV
import webbrowser as web

# ---------------- CONTEXT --------------------
# Program: Contact Tracing App
# 	- Create a python program that will read QRCode using your webcam
# 	- You may use any online QRCode generator to create QRCode
# 	- All personal data are in QRCode 
# 	- You may decide which personal data to include
# 	- All data read from QRCode should be stored in a text file including the date and time it was read

cap = CV.VideoCapture(0)

img_QRdetect = CV.QRCodeDetector()

while True:
    _, img = cap.read()

    data, bbox, _ = img_QRdetect.detectAndDecode(img)
    if data:
        a = data
        with open("QR_Logs.txt", "w") as txtfile:
            txtfile.write(a)
        break
    CV.imshow("QRCODE_Scanner", img)
    if CV.waitKey(1) == ord("q"):
        break

bb = web.open(str(a))
cap.release()
CV.destroyAllWindows()