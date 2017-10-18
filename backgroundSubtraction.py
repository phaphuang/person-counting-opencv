import numpy as np
import cv2
INST_WIDTH = 800
INST_HEIGHT = 600
maiorArea = 0
cap = cv2.VideoCapture('../src/mycctv01.avi')

ret, frame = cap.read()
frame = cv2.resize(frame, (INST_WIDTH, INST_HEIGHT))
backimg = cv2.imread('../src/bg_office.png')
backimg = cv2.resize(frame, (INST_WIDTH, INST_HEIGHT))
fundo = cv2.GaussianBlur(backimg,(3,3),0)

"""
if not(cap.isOpened()):
    cap.open()

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (INST_WIDTH, INST_HEIGHT))
    cv2.imshow("Webcam", frame)
    bkg=frame.copy()
    fundo = cv2.GaussianBlur(bkg,(3,3),0)
    print("OK")
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyWindow("Webcam")
        break
"""

while True:
    ret, imagem = cap.read()
    imagem = cv2.resize(imagem, (INST_WIDTH, INST_HEIGHT))
    mascara=imagem.copy()
    cinza=imagem.copy()
    #cv2.imshow("Webcam", imagem)
    imagem = cv2.GaussianBlur(imagem,(3,3),0)
    cv2.absdiff(imagem,fundo,mascara)
    gray = cv2.cvtColor(mascara, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8)
    dilated = cv2.dilate(thresh1,kernel,iterations = 5)
    cinza = cv2.erode(dilated,kernel,iterations = 3)
    _,contorno,heir=cv2.findContours(cinza,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contorno:
        print cv2.contourArea(cnt)
        vertices_do_retangulo = cv2.boundingRect(cnt)
        if (cv2.contourArea(cnt) > 10000 and cv2.contourArea(cnt) < 15000):
            #maiorArea = cv2.contourArea(cnt)
            #retangulo_de_interesse = vertices_do_retangulo

            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(imagem, (cx, cy), 5, (0,0,255), -1)
            img = cv2.rectangle(imagem, (x, y), (x+w, y+h), (0,255,0), 2)

        #ponto1 = (retangulo_de_interesse[0], retangulo_de_interesse[1])
        #ponto2 = (retangulo_de_interesse[0] + retangulo_de_interesse[2], retangulo_de_interesse[1] + retangulo_de_interesse[3])
        #cv2.rectangle(imagem, ponto1, ponto2,(0,0,0), 2)
        #cv2.rectangle(cinza, ponto1, ponto2, (255,255,255), 1)
        #largura = ponto2[0] - ponto1[0]
        #altura = ponto2[1] - ponto1[1]
        #cv2.line(cinza,(ponto1[0]+largura/2,ponto1[1]),(ponto1[0]+largura/2,ponto2[1]),(255,255,255), 1)
        #cv2.line(cinza,(ponto1[0],ponto1[1]+altura/2),(ponto2[0],ponto1[1]+altura/2), (255,255,255), 1)

    cv2.imshow("Mascara", mascara)
    cv2.imshow("Cinza", cinza)

    cv2.imshow("Webcam", imagem)
    cv2.imshow("Dilated", thresh1)
    #cv2.imshow("Fundo", dilated)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break


# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
