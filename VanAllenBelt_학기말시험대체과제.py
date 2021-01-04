#Van Allen Belt에서 전하 운동 시뮬레이션
#기초물리응용_김창배교수님_20181311김규동

def setup_physics() :
    global magnetic_const, mp, qp, E_magnetic_moment, Re, kin_enrg, v0
    magnetic_const = 1.e-7    #자기장상수
    mp = 1.67e-27    #양성자 질량
    qp = 1.60e-19    #양성자 전하량
    E_magnetic_moment = 7.94e22*vector(0,-1,0) #지구 자기 모멘트
    Re = 6378137      #지구 반지름
    kin_enrg =  6.e7*1.6e-19  #양성자에너지
    v0 = sqrt(2*kin_enrg/mp)  #양성자속력

def setup_scene() :
    global L
    L = 3 * Re
    scene.height = scene.width = 600
    scene.range = L

def make_objects() :
    global earth, q1
    earth = sphere(pos=vector(0,0,0), radius=Re, color=color.green, #지구
               texture=textures.earth, opacity=0.3, shininess = 1, emissive=True)
    q1 = sphere(radius=0.02*Re, color=color.red, make_trail=True) # 양성자

def init() :
    global t
    q1.pos = vector(2.5*Re, 0, 0)    #양성자 위치
    q1.v = v0*vector(sqrt(1/2.), sqrt(1/2.), 0)   #양성자 속도
    t = 0

setup_physics()
setup_scene()
make_objects()
init()

scene.waitfor('click')
while (t<3) :
    rate(10000)
    r = mag(q1.pos)
    B = magnetic_const*(3*dot(E_magnetic_moment,q1.pos)*q1.pos/r**5 - E_magnetic_moment/r**3) #자기장
    freq = abs(qp/mp)*mag(B)  #진동수
    dt = .002/freq  #시간증분
    q1.v += dt*qp/mp*cross(q1.v, B)
    q1.pos += dt*q1.v
    t += dt
print("한학기동안 감사했습니다!")



