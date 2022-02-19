import cv2 as CV
import webbrowser as web
import datetime, os, numpy
from pyzbar import pyzbar

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

def read_barcodes(frame):
    QRPatterDt = pyzbar.decode(frame)
    TempVar = [""]
    for code in QRPatterDt:
        QRInfo = code.data.decode('utf-8')
        TempVar.append(QRInfo)
        boxPnt = numpy.array([code.polygon],numpy.int32)
        boxPnt = boxPnt.reshape((-1, 1, 2))
        CV.polylines(image, [boxPnt], True, (0, 255, 0), 4)

        boxPnt0 = code.rect
        CV.putText(image, QRData, (boxPnt0[0], boxPnt0[1]), CV.FONT_HERSHEY_COMPLEX_SMALL, 0.9, (0, 15, 0), 2)
    return frame, TempVar[-1]

qrCapt = CV.VideoCapture(0)
qrCapt.set(3, 650)
qrCapt.set(4, 480)

while True:
    etc_, image = qrCapt.read()
    
    image, QRData = read_barcodes(image)
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
    if CV.waitKey(5) == ord("p"):
        break

try:
    redirectBrwsr = web.open(DecodedDataQR)
    print("\33[92mRedirecting to Contents :)\33[0m")
    qrCapt.release()
    CV.destroyAllWindows()
except Exception as e:
        print(f"\33[91mCancelled Operation :(\33[0m")
