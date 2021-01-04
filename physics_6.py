
# physics parameters
def setup_physics():
    global e_const, Q, R, charge, mass
    e_const = 9.e9  # 쿨롱 상수
    Q = 3.e-9  # 고리 전하량
    R = 0.1  # 고리 반지름
    charge = -1.e-9  # 점전하 전하량
    mass = 1.e-9  # 점전하 질량


# 화면 설정
def setup_scene():
    scene.height = scene.width = 600  # 창의 높이, 폭
    scene.range = 1.5 * R  # 창의 스케일


# 고리
def make_ring():
    global ring, point_charge
    ring = curve(radius=R / 50, color=color.orange, q=Q)  # 고리를 그리기 전 사전 작업
    N = 100  # 고리 부분들의 숫자
    d_theta = 2 * pi / N  # 각도를 조금씩 증가
    theta = 0
    while theta <= 2 * pi:
        ring.append(pos=R * vector(0, cos(theta), sin(theta)))  # 각 부분의 시작 위치 지정
        theta += d_theta

    # 점 전하


def make_charge():
    global point_charge
    point_charge = sphere(radius=4 * ring.radius, color=color.red)  # 점전하
    point_charge.q = charge  # 전하량
    point_charge.m = mass  # 질량


# 그래프 설정
def setup_graphics():
    global xt_graph, fx_graph, Ex_graph, Ex_graph1, Ex_graph2
    # 그래프 창
    xt_display = gdisplay(title='x vs t', xtitle='time', ytitle='position',
                          x=600, y=0, width=600, height=300)
    fx_display = graph(title='F vs x', xtitle='position', ytitle='force',
                       x=600, y=300, width=600, height=300)
    Ex_display = graph(title="Energy vs x", xtitle='position', ytitle="Energy",
                       width=600, height=300)
    # 플롯 함수
    xt_graph = gdots(gdisplay=xt_display, color=color.cyan)  # x vs t
    fx_graph = gdots(graph=fx_display, color=color.green)  # force vs x
    Ex_graph = gdots(graph=Ex_display, color=color.red)
    Ex_graph1 = gdots(graph=Ex_display, color=color.cyan)
    Ex_graph2 = gdots(graph=Ex_display, color=color.green)


# 초기 조건
def init():
    global t, dt, r0, flow_ctrl
    r0 = vector(1 * R, 0, 0)  # 초기 위치
    point_charge.pos = r0  # 초기위치
    point_charge.v = vector(0, 0, 0)  # 초기속도
    dt = 1.e-4  # 시간 증분
    t = 0  # 초기 시간
    flow_ctrl = 'PAUSE'


# 전위와 전기장
# curve()로 구성한 obj의 전위와 전기장
def pot_and_field(obj, pt):
    n = obj.npoints - 1  # 조각난 부분들의 수
    dq = obj.q / n  # 각 부분의 전하량(균일)
    e_fld = vector(0, 0, 0)  # 전기장
    poten = 0  # 전위
    for j in range(n):  # 각 부분의 전기장의 벡터 합과 전위의 합
        dl = obj.point(j + 1).pos - obj.point(j).pos
        rs = obj.point(j).pos + dl / 2  # 각 부분의 중앙의 위치
        r = pt - rs  # 각 부분의 중앙의 위치에 대한 점전하의 상대 위치
        r_hat = norm(r)  # r/mag(r)
        e_j = r_hat * (e_const * dq / mag(r) ** 2)  # 각 부분이 점전하가 있는 곳에 만드는 전기장
        e_fld += e_j
        p_j = e_const * dq / mag(r)  # 각 부분이 점전하가 있는 곳에 만드는 전위
        poten += p_j
    return poten, e_fld


def widget_play():
    global button_run, button_stop
    button_run = button(text='Run', pos=scene.title_anchor, bind=run_pause)
    scene.append_to_title('  ')
    button_stop = button(text='Stop', pos=scene.title_anchor, bind=stop)


def run_pause(evt):
    global flow_ctrl
    if flow_ctrl == 'RUN':
        flow_ctrl = 'PAUSE'
        button_run.text = 'Run'
    else if flow_ctrl == 'PAUSE':
        flow_ctrl = 'RUN'
        button_run.text = 'Pause'


def stop(evt):
    global flow_ctrl
    button_run.disabled = True
    button_stop.disabled = True
    flow_ctrl = 'STOP'


###################################
setup_physics()
setup_scene()
make_ring()
make_charge()
setup_graphics()
init()
widget_play()
# 힘 화살표
f_arrow = arrow(pos=point_charge.pos, color=color.green, visible=False)
f_arrow.shaftwidth = point_charge.radius / 2.
scale_factor = 5.e4
cycle = False

# 운동
# scene.waitfor('click')
while True:
    rate(100)
    if (flow_ctrl == 'RUN'):
        xt_graph.plot(pos=(t, point_charge.pos.x))  # x vs t
        # 전위와 전기장
        f_arrow.visible = False
        poten, e_fld = pot_and_field(ring, point_charge.pos)
        E_p = poten * charge
        E_k = (point_charge.v.x) ** 2 * 0.5 * mass
        E_t = E_p + E_k
        Ex_graph.plot(pos=(point_charge.pos.x, E_p))  # red 음의 포텐셜 에너지(서로 반대 부호임을 의미)
        Ex_graph1.plot(pos=(point_charge.pos.x, E_k))  # cyan 운동 에너지
        Ex_graph2.plot(pos=(point_charge.pos.x, E_t))
        # green 역학적 에너지의 값은 속도 = 0일때 운동을 시작한 지점의 위치에너지의 값과 같다. 역학적 에너지는 보존된다!!!
        if cycle == False:
            if point_charge.v.x > 0:
                print("주기 :", t * 2)  # 주기의 절반 *
                print("식으로 구한 주기 :",
                      1 / ((e_const * Q * charge * -1 / (mass * R ** 3)) ** 0.5 / (2 * pi)))  # 637쪽 33번문제식을 이용한 1/진동수
                print(
                    "차이가 나는 이유는 637쪽 33번문제에서 x 보다(이 프로그램에서 점전하의 시작 위치) a가 훨씬 크다는 가정을 하고 있기 때문이다.\n실제로 점전하의 시작 위치를 반지름 값보다 작게 할 경우 교재의 해당 수식을 통해 구한 주기와 비슷한 값이 나오게 된다!")
                cycle = True

        # 전기력
        force = point_charge.q * e_fld  # 점전하가 받는 힘
        fx_graph.plot(pos=(point_charge.pos.x, force.x))  # 힘과 위치 그래프
        f_arrow = arrow(pos=point_charge.pos, color=color.green, axis=scale_factor * force)
        # 위치 이동
        point_charge.v.x += force.x / point_charge.m * dt  # 속도
        point_charge.pos.x += point_charge.v.x * dt  # 위치
        t += dt
    elif (flow_ctrl == 'STOP'):
        break
