import cv2
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# chiều rộng và chiều cao của camera
wCam,hCam =  680,480
import HandTracking as htm
import pyautogui
import  numpy as np

cam = cv2.VideoCapture(0)

detector = htm.handDetector(maxHands=1)

fingers_number = [4,8,12,16,20]

# các giá trị để làm min
smoothening = 5
# chiều rông và chiều cao của màn hình máy tính
wScreen,hScreen =  pyautogui.size()

drag = False
has_started = False
has_grabbed = False
check = True

while True:
    success, frame = cam.read()

    # lật ngược lại camera
    image = cv2.flip(frame,1)

    # xác định vị trí bàn tay trên webcam 
    image = detector.findHands(image)
    lamark_list = detector.findPosition(image,draw=False)
    
    # kiểm tra sự tồn tại của bàn tay
    if len(lamark_list)!=0:
        # xác định tọa độ ngón trỏ
        x1,y1=lamark_list[8][1:]
        x2,y2=lamark_list[4][1:]
        # Kiểm tra tọa độ của điểm 0 và 17 (nếu có)
        if len(lamark_list) >= 18:
            x0, y0 = lamark_list[0][1], lamark_list[0][2]
            x17, y17 = lamark_list[17][1], lamark_list[17][2]
        # xác định  sự co duỗi của các ngón tay
        fingers = [] # [0,1,0,0,0]
        # xác định ngón cái
        if lamark_list[fingers_number[0]][1] < lamark_list[fingers_number[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # xác định 4 ngón còn lại
        for id_finger in range(1,5):
            if lamark_list[fingers_number[id_finger]][2] < lamark_list[fingers_number[id_finger]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # vẽ 1 HCN nhỏ trên cam tượng trưng cho  với màn hình máy tính
        cv2.rectangle(image,(100,50),(wCam-100,hCam-190),(0,0,0),2) 

        # Chuyên đổi tọa độ của  ngón trỏ  trên màn hình webcam để tương ứng với màn hình máy tính 
        x3=np.interp(x1,(100,wCam-100),(0,wScreen))
        y3=np.interp(y1,(50,hCam-190),(0,hScreen))

        # Làm mịn các giá trị
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        if x1 > 100 and x1 < wCam-100 and y1 > 50 and y1 < hCam-190:
            # cuộn chuột xuống  khi chỉ có ngón trỏ và ngón giữa chạm vào trục hoành bên trên hình chữ nhật
            if x1 > 100 and x1 < wCam-100 and y1 > 50 and y1 < 60:
                if fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0:
                    pyautogui.scroll(100)
        
            # cuộn chuột xuống  khi chỉ có ngón trỏ và ngón giữa chạm vào trục hoành bên dưới hình chữ nhật
            if x1 > 100 and x1 < wCam-100 and y1 > hCam-210 and y1 < hCam-190:
                if fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0:
                    pyautogui.scroll(-100)
                    
            # Vùng chuyển cửa sổ bên trái
            if x0 > 100 and x0 < 120 and y0 > 50  and y0 < hCam-190:
                pyautogui.press('left')
            # Vùng chuyển cửa sổ bên phải
            if x0 > wCam-110 and x0 < wCam-100 and y0 > 50 and y0 < hCam-190:
                pyautogui.press('right')
                    
            # tắt giữ chuột trái
            if drag == True and fingers.count(0) != 5:
                drag = False
                pyautogui.mouseUp(button = "left")
    
            # Chỉ ngón trỏ có Chế độ di chuyển
            if  fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:            
                pyautogui.moveTo(clocX,clocY)
                cv2.circle(image,(x1,y1),10,(0,255,0),-1)  
                plocX, plocY = clocX, clocY
    
          
            flag = False
    
            # click chuột trái khi ngón 1,2 chạm nhau
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0  and fingers[4]== 0:
                # Tìm khoảng cách giữa các ngón tay
                length, img, lineInfo = detector.findDistance(8, 12, image) 
                if length < 27 and not flag:
                    cv2.circle(image,(lineInfo[4],lineInfo[5]),10,(0,255,0),-1)
                    pyautogui.click()
                    flag = True
            # click chuột phải
            elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0  and fingers[4]== 1:
                # Tìm khoảng cách giữa các ngón tay
                length, img, lineInfo = detector.findDistance(8, 12, image)    
                if length < 27 and not flag:
                    cv2.circle(image,(lineInfo[4],lineInfo[5]),10,(0,255,0),-1)
                    pyautogui.click(button="right") 
                    flag = True
            else:
                flag = False
    
    
            # doubleClick chuột khi chỉ có ngón trỏ , ngón giữa được duỗi  và khoảng cách < 27
            if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0  and fingers[4]== 0:
                # Tìm khoảng cách giữa các ngón tay
                length, img, lineInfo = detector.findDistance(8, 12, image) 
                if length < 27:
                    cv2.circle(image,(lineInfo[4],lineInfo[5]),10,(0,255,0),-1)
                    pyautogui.click()
                    flag = True
                    
            # enter
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1  and fingers[4]== 1:
                pyautogui.press('enter')
                
    
            # # cuộn chuột lên khi chỉ có ngón cái , ngón trỏ được duỗi 
            # elif fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            #     pyautogui.scroll(100)
    
            # # cuộn chuột xuống  khi chỉ có ngón trỏ , ngón út được duỗi 
            # elif fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            #     pyautogui.scroll(-100)                                 
    
            # Kéo thả Chuột 
            drag = False
            
            if fingers[0] == 1 and fingers[1] == 1 and fingers.count(0) == 3 and drag == False:
                length, img, lineInfo = detector.findDistance(4, 8, image) 
                if length < 27 and not drag:
                    cv2.circle(image,(lineInfo[4],lineInfo[5]),10,(0,255,0),-1)
                    pyautogui.mouseDown(button="left")                
                    flag = True
            # thả chuột
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1  and fingers.count(0) == 3 and drag == True:
                length, img, lineInfo = detector.findDistance(4, 12, image) 
                if length < 27 and drag:
                    cv2.circle(image,(lineInfo[4],lineInfo[5]),10,(0,255,0),-1)
                    pyautogui.mouseUp(button="left")
                    flag = False
                    
            # trở về màn hình windows khi bàn tay nắm lại
            if fingers.count(0) == 5 and not has_grabbed:
                pyautogui.hotkey('win', 'd')
                has_grabbed = True
                
            # Khi người dùng đã nắm ít nhất một lần, đánh dấu biến has_started = True
            if not has_started and has_grabbed:
                has_started = True
                
            # Nếu đã bắt đầu, và người dùng buông tay, reset biến has_grabbed để cho phép lệnh được thực hiện lại khi người dùng nắm lần tiếp theo
            if has_started and fingers.count(0) != 5 and has_grabbed:
                has_grabbed = False
            
            # Thực hiện win + tab
            if fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and check == True:
                pyautogui.hotkey('win', 'tab')
                check = False
            elif fingers[0]!=0 or fingers[1]!=0 or fingers[2]!=1 or fingers[3]!=1 or fingers[4]!=1:
                check = True
                

    # hiện thị camera
    cv2.imshow("Virtual Mouse" ,image)
    # màn hình camera luôn được hiển thị trên cùng
    cv2.setWindowProperty("Virtual Mouse",cv2.WND_PROP_TOPMOST,1)
    # tắt chương trình khi nhấn "q"
    if cv2.waitKey(1) == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()    