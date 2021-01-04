#기초물리응용_김창배교수님_20181311_김규동_과제 1., 2.

def setup_physics():
    global charge, mass, kin_enrg, B_vector, E_vector, v_d, T
    charge = 1.6e-19 #양성자 전하량
    mass = 1.67e-27 #양성자 질량
    kin_enrg = 1.e6*1.6e-19 #운동에너지 1MeV
    B_vector = 1.e-5*vector(0, 0, 1) #자기장 벡터
    E_vector = 1*vector(0, 1, 0) #전기장 벡터
    v_d = mag(E_vector)/mag(B_vector) #유동속도 이론값
    T = 2*pi*mass/(charge*mag(B_vector)) #주기 이론값

def setup_scene():
    global L
    L = sqrt(2*mass*kin_enrg)/(charge*mag(B_vector)) #gyro-radius 1.e4
    scene.height = scene.width = 600 #창의 높이, 폭
    scene.range = 2*L

def setup_graphics():
    global xt_graph, yt_graph, fx_graph, Px_graph, Kx_graph, Mx_graph
    xt_display = gdisplay(title='position vs time', xtitle='time', ytitle='x, y',
                           x=600, y=0, width=600,height=300)
    ex_display = gdisplay(title='Energy vs x', xtitle='x', ytitle='energy',
                             x=600, y=600, width=600,height=300)
    #플롯 함수
    xt_graph = gdots(gdisplay=xt_display, color=color.yellow, interval=20)#x vs t
    yt_graph = gdots(gdisplay=xt_display, color=color.green, interval=20)#y vs t
    Px_graph = gdots(gdisplay =ex_display, color=color.red, interval=20)#PE vs x
    Kx_graph = gdots(gdisplay =ex_display, color=color.blue, interval=20)#KE vs x
    Mx_graph = gdots(gdisplay =ex_display, color=color.green, interval = 20)#ME vs x

def make_objects():
    global q1
    q1 = sphere(radius= L/12., color=color.yellow, make_trail=True, interval=50, \
                trail_type="points")
    q1.q = charge #전하량
    q1.m = mass #질량
    
   
def init():
    global t, dt, v_d, q1_st
    q1.pos = 1.2*L*vector(-1, 0, 0) #초기 위치
    q1_st = q1.pos.x #초기 위치 저장
    q1.v = sqrt(2*kin_enrg/q1.m)*vector(0, 1, 0) #초기 속도 1MeV
    dt = 1.e-3/(abs(q1.q)*mag(B_vector)/q1.m) #시간 증분
    t = 0 #초기 시간

#fields
def E_and_B_field(pt):
    return E_vector, B_vector


##############################################

setup_physics()
setup_scene()
setup_graphics()
make_objects()
init()

scene.waitfor('click')
#운동
while True :
    rate(5000)
    xt_graph.plot(pos=(t, q1.pos.x)) #x vs t
    yt_graph.plot(pos=(t, q1.pos.y)) #y vs t
    E, B = E_and_B_field(q1.pos)
    em_force = q1.q*(E +cross(q1.v, B)) #전자기력
    p_enrg = -q1.q *E.y*q1.pos.y # PE 전기 퍼텐셜 에너지
    k_enrg = q1.m*mag(q1.v)**2/2#KE 운동에너지
    m_enrg = p_enrg + k_enrg # ME 역학에너지
    Px_graph.plot(pos=(q1.pos.x, p_enrg)) #전기퍼텐셜에너지 vs x red
    Kx_graph.plot(pos=(q1.pos.x, k_enrg)) #운동에너지 vs x blue
    Mx_graph.plot(pos=(q1.pos.x, m_enrg)) #역학에너지 vs x green
    q1.v += (em_force/q1.m)*dt #속도 업데이트
    q1.pos += q1.v*dt #위치 업데이트
    t += dt
    if (2*T-dt <= t)&(t < 2*T) : 
        v_d_simul = (q1.pos.x-q1_st)/(t) # 시뮬레이션 유동속도
        print("역학적에너지는 보존된다!(점 전하의 운동에너지가 변하지 않는다.)")
        print("점전하의 x방향으로의 유동속도는 {:.2e}m/s".format(v_d_simul))
        print("이론적인 유동속도는 {:.2e}m/s".format(v_d))
        print("오차율은 {:.2e}%이다.".format((v_d_simul-v_d)/v_d*100))
