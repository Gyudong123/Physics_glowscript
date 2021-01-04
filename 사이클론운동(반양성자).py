#기초물리응용_김창배교수님_20181311_김규동_과제 3. 반양성자

def setup_physics():
    global charge, mass, kin_enrg, B_vector, E_vector, v_d, T
    charge = 1.6e-19 #반양성자 전하량
    mass = 1.67e-27 #양성자 질량
    kin_enrg = 1.e6*1.6e-19 #운동에너지 1MeV
    B_vector = 1.e-5*vector(0, 0, 1) #자기장 벡터


def setup_scene():
    global L
    L = sqrt(2*mass*kin_enrg)/(charge*mag(B_vector)) #gyro-radius 1.e4
    scene.height = scene.width = 600 #창의 높이, 폭
    scene.range = 4*L

def setup_graphics():
    global xt_graph, yt_graph, fx_graph, Px_graph, Kx_graph, Mx_graph
    xt_display = gdisplay(title='position vs time', xtitle='time', ytitle='x, y',
                           x=600, y=0, width=600,height=300)
    ex_display = gdisplay(title='Energy vs x', xtitle='x', ytitle='energy',
                             x=600, y=600, width=600,height=300)
    #플롯 함수
    xt_graph = gdots(gdisplay=xt_display, color=color.yellow, interval=20)#x vs t
    yt_graph = gdots(gdisplay=xt_display, color=color.green, interval=20)#y vs t
    Kx_graph = gdots(gdisplay =ex_display, color=color.blue, interval=20)#KE vs x

def make_objects():
    global q1
    q1 = sphere(radius= L/12., color=color.yellow, make_trail=True, interval=50, \
                trail_type="points")
    q1.q = -charge #전하량
    q1.m = mass #질량
    
   
def init():
    global t, dt, v_d, q1_st
    q1.pos = 1.2*L*vector(-1, 0, 0) #초기 위치
    q1_st = q1.pos.x #초기위치 저장
    q1.v = sqrt(2*kin_enrg/q1.m)*vector(0, 1, 0) #초기 속도 1MeV
    dt = 1.e-3/(abs(q1.q)*mag(B_vector)/q1.m) #시간 증분
    t = 0 #초기 시간

#fields
def B_field(pt):
    B_vector_uneven = (1 - pt.y/(40*L))*B_vector
    return B_vector_uneven


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
    B = B_field(q1.pos)
    m_force = q1.q*(cross(q1.v, B)) #자기력
    k_enrg = q1.m*mag(q1.v)**2/2#KE 운동에너지
    Kx_graph.plot(pos=(q1.pos.x, k_enrg)) #운동에너지 vs x blue
    q1.v += (m_force/q1.m)*dt #속도 업데이트
    q1.pos += q1.v*dt #위치 업데이트
    t += dt
    if (q1.pos.y <0)&(q1.pos.y+q1.v.y*dt > 0) : 
        v_d_simul = (q1.pos.x-q1_st)/t # 시뮬레이션 유동속도
        print("점전하의 x방향으로의 유동속도는 {:.2e}m/s".format(v_d_simul))
        print("점전하의 운동에너지가 점점 커진다!")
        print("점전하의 부호가 바뀐 경우 유동 방향이 바뀐다.")

