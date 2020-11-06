GlowScript 3.0 VPython 
#지구의 공전 운동 시뮬레이션 
#태양은 원점에 정지 
#근일점 데이터 사용 
#2020-10-01
#physics parameters 

def setup_physics():
    global G, m_s, m_e, r_ap, r_peri, T, enrg, v_ap, v_peri, angular_speed
    G = 6.674e-11 #만유인력상수 
    m_s = 1.989e30 #태양의 질량 
    m_e = 5.97e24 #지구의 질량 
    r_ap = 1.521e11 #원일점 
    r_peri = 1.471e11 #근일점
    T = 3.156e7 #공전 주기(초) 
    a = (r_ap+r_peri)/2. #지구 궤도의 장반경, 1,496e11 
    enrg = -G*m_s*m_e/(2*a) #지구의 에너지: 운동 + 위치(퍼텐셜) 
    v_ap = 2.929e4 
    v_peri = 3.029e4
    angular_speed = 2*pi/(24*60*60) #자전 각속도
    
def setup_scene():
    global L
    scene.height = scene.width = 600 #화면의 세로 가로 (픽셀)
    L = 1.2*r_ap
    scene.range = L #화면의 크기(미터)
    
def make_objects():
    global sun, earth
    sun = sphere(radius=L/50., pos=vector(0,0,0), color = color.red) #태양
    earth = sphere(radius=L/10., color=color.green, make_trail=True,
    trail_type="points", interval=10,
    texture=textures.earth) #지구
    earth.theta = radians(23.4) #자전축의 각도

def init():
    global t, dt, fps
    r0 = vector(r_peri, 0, 0) #근일점 좌표
    v0 = vector(0, v_peri, 0) #근일점 지구 속도 
    earth.pos = r0 #지구 위치
    earth.vel = v0 #지구 속도
    t = 0 #시작 시간
    dt = T/1000 #시간 변화량
    fps = 100 #frames per second
 
def setup_graphics() :
    global KE_graph, PE_graph, TE_graph, L_graph
    #그래프 창
    enrg_display = graph(title = 'Angular momentum vs r', xtitle = 'r', ytitle = 'Am(단위:1e32)', 
    x = 600, y =0, width = 600, height = 400, xmin = 0.999*r_peri, xmax = 1.001 * r_ap)
    enrg_display2 = graph(title = 'Energy vs t', xtitle = 't', ytitle = 'Energy',
    x = 600, y = 0, width = 600, height  = 400, xmin = 0, xmax = T)
    
    #플롯 함수
    KE_graph = gdots(graph = enrg_display2, color = color.cyan) 
    PE_graph = gdots(graph = enrg_display2, color = color.blue)
    TE_graph = gdots(graph = enrg_display2, color = color.red)
    L_graph = gdots(graph = enrg_display, color = color.black)
    
    
setup_physics()
setup_scene()
make_objects()
setup_graphics()
init()

scene.waitfor('click')
while True :
    rate(fps) #1초 당 fps 반복
    r = mag(earth.pos) #태양과 지구 사이 거리
    rhat = norm(earth.pos) #태양에서 바라본 지구 방향
    enrg_kin = 0.5*m_e*mag(earth.vel)**2 #운동에너지
    enrg_pos = -G*m_e*m_s/r
    enrg_tot = enrg_kin + enrg_pos
    KE_graph.plot(pos=(t, enrg_kin)) #운동에너지 플롯
    PE_graph.plot(pos=(t,enrg_pos))
    TE_graph.plot(pos=(t,enrg_tot)) #에너지는 보존됩니다!
    L = m_e *((earth.pos.x * earth.vel.y - earth.pos.y * earth.vel.x)) //1e32 #각운동량은 보존됩니다!
    L_graph.plot(pos = (r,L))
    
    earth.vel += -(G*m_s/r**2)*rhat*dt #지구 속도 업뎃
    earth.pos += earth.vel*dt #지구 위치 업뎃
    earth.rotate(angle = angular_speed*dt, axis= vector(sin(earth.theta),cos(earth.theta),0))
    t += dt #시간 업뎃
