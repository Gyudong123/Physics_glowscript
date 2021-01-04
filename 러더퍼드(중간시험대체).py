
def setup_physics():
    global k_e, m_alpha, m_Au, q_alpha, q_Au, r_alpha, r_Au
    k_e = 8.988e9                   #쿨롱 상수
    m_p = 1.673e-27                       #양성자 질량
    m_n = m_p                                #중성자 질량
    m_alpha = 2*m_p + 2*m_n        #알파 입자의 질량
    m_Au = 79*m_p + 117*m_n       #금 원자 핵의 질량
    q_p = 1.602e-19                          #양성자 전하량
    q_alpha = 2*q_p                       #알파 입자 전하량
    q_Au = 79*q_p                          #금 원자 핵의 질량
    r_alpha = (4**(1/3))*1.2e-15           #알파 입자의 반지름
    r_Au = ((79+117)**(1/3))*1.2e-15     #금 원자핵의 반지름

def setup_scene():
    global L
    L = 100*r_Au
    scene.range = L #화면의 크기

def make_objects():
    global alpha, Au
    alpha = sphere(radius=5*r_alpha, m=m_alpha, q=q_alpha, color=color.green, make_trail=True,
               trail_type="points", interval=10)             #알파 입자
    Au = sphere(pos=vector(0,0,0), radius=3*r_Au, m=m_Au, q=q_Au, color=color.yellow)  # 금 원자핵
   
def init():
    global t, dt, fps, v_alpha
    v_alpha = 1e7             #알파 입자의 속력
    r0 = vector(-0.99*L, 3*r_Au, 0)  #알파 입자의 초기 위치
    v0 = vector(v_alpha, 0, 0)         #알파 입자의 초기 속도
    alpha.pos = r0                      #알파 입자 초기 위치
    alpha.vel = v0                      #알파 입자 초기 속도
    T = L/v_alpha             # 화면을 통과 하는데 걸리는 시간
    t = 0 #시작 시간
    dt = T/1000
    fps = 1000


###########################################################

setup_physics()
setup_scene()
make_objects()
init()

scene.waitfor('click')
while alpha.pos.x<=0.99*L and abs(alpha.pos.y)<=0.99*L:
    rate(fps) #1초 당 fps 반복
    r = mag(alpha.pos -Au.pos) #두 입자 사이 거리
    rhat = norm(alpha.pos -Au.pos) #금 -> 알파
    alpha.vel += dt*(k_e*alpha.q*Au.q/r**2)*rhat/alpha.m #알파 속도 업뎃
    alpha.pos += dt*alpha.vel #알파 위치 업뎃
    t += dt #시간 업뎃


scatter_angle = atan2(alpha.pos.y, alpha.pos.x)
print("산란각 = ", degrees(scatter_angle)+'도')




