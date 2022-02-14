import cv2 as CV
import webbrowser as web
import datetime, os

# ---------------- CONTEXT --------------------
# Program: Contact Tracing App
# 	- Create a python program that will read QRCode using your webcam
# 	- You may use any online QRCode generator to create QRCode
# 	- All personal data are in QRCode 
# 	- You may decide which personal data to include
# 	- All data read from QRCode should be stored in a text file including the date and time it was read

def StoreDatatoTxt (data, sv_method):
    if (sv_method == None) or (sv_method == 0):
        sv_method = "w"
    elif (sv_method == 1) or (sv_method == True):
        sv_method = "a"
    with open("QR_Logs.txt", sv_method) as txtfile:
        crrnt_time = datetime.datetime.now()
        if sv_method == "w":
            txtfile.write(f"Accessed {data} \n Time: {crrnt_time}")
        elif sv_method == "a":
            txtfile.write(f"\nAccessed {data} \n Time: {crrnt_time}")

qrCapt = CV.VideoCapture(0)
qrCapt.set(3, 650)
qrCapt.set(4, 480)

img_QRdetect = CV.QRCodeDetector()

while True:
    _, image = qrCapt.read()
    
    QRData, CoordBox, _ = img_QRdetect.detectAndDecode(image)
    if QRData:
        DecodedDataQR = QRData
        try:
            verifyFl = os.path.exists("QR_Logs.txt")
            if verifyFl == True:
                    verifyCtnt = os.path.getsize("QR_Logs.txt")
                    if verifyCtnt == 0:
                        StoreDatatoTxt(DecodedDataQR, 0)
                        break
                    else:
                        StoreDatatoTxt(DecodedDataQR, 1)
                        break
            elif verifyFl == False:
                    StoreDatatoTxt(DecodedDataQR, 0)
                    break
        except Exception as e:
            print(f"\33[91mAn error occured :( ---> {e}\33[0m")
            break
    CV.imshow("QRCODE_Scanner", image)
    if CV.waitKey(1) == ord("s"):
        break

bb = web.open(str(DecodedDataQR))
qrCapt.release()
CV.destroyAllWindows()