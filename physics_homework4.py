GlowScript 3.0 VPython

def rad(degrees): #converts an angle in degrees to an angle in radians
    radians=degrees*pi/180
    return radians
def collisionSphereAndBox(sphereObj,boxObj) :
    xs = sphereObj.pos.x
    ys = sphereObj.pos.y
    xb = boxObj.pos.x
    yb = boxObj.pos.y
    rs = sphereObj.radius
    lb = boxObj.length
    hb = boxObj.height
    wb = boxObj.width
    if(abs(xs-xb)<rs+lb/2 and abs(ys-yb) < rs +hb/2) :
        return True
    else :
        return False
        

def make_label(x=0, y=0, text= '', centered=False):
    l=None
    if centered:
        l= label(pos=vector(x,y,0), opacity=0, box=0, line=0)
    else:
        l= label(pos=vector(x,y,0), xoffset=1, opacity=0, box=0, line=0)
    l.text= text
    l.font = 'sans'; l.height = 15
    return l

def key_ctrl(evt):
    global turret, angleBar,muzzlespeed, speedBar, buttet, bulletsList, lbl
    k = evt.key
    if k=="up":
        turret.theta += turret.dtheta
        turret.axis = turret.L*vector(cos(turret.theta),sin(turret.theta),0)
        angleBar.axis=(5*turret.theta)*vector(1,0,0)
    elif k=="down":
        turret.theta += -turret.dtheta 
        turret.axis = turret.L*vector(cos(turret.theta),sin(turret.theta),0)
        angleBar.axis=(5*turret.theta)*vector(1,0,0)
    elif k=="left":
        muzzlespeed += -dspeed
        speedBar.axis = (muzzlespeed/2.+0.5)*vector(1,0,0)
    elif k=="right":
        muzzlespeed += dspeed
        speedBar.axis=(muzzlespeed/2.+0.5)*vector(1,0,0)
    elif k==" ":
        bullet = sphere(pos=turret.pos+turret.axis, radius=0.5, color=color.white)
        bullet.v = muzzlespeed*vector(cos(turret.theta),sin(turret.theta),0)
        bullet.ptd = False
        lbl.text = ""
        bulletsList.append(bullet)

scene.range = 20
scene.width = 600
scene.height = 600

#create objects
ground = box(pos=vector(0,-15,0), size=vector(40,1,2), color=color.green)
tank = box(pos=vector(-18,ground.pos.y+2,0), size=vector(2,2,2), color=color.yellow)
turret = cylinder(pos=tank.pos, axis=vector(0,0,0), radius=0.5, color=tank.color)
turret.pos.y = turret.pos.y+tank.height/2
angleBar = cylinder(pos=vector(-18,ground.pos.y-2.5,0), axis=vector(1,0,0), radius=1, color=color.magenta)
speedBar = cylinder(pos=vector(5,ground.pos.y-2.5,0), axis=vector(1,0,0), radius=1, color=color.cyan)
target = box(pos = tank.pos+vector(-2*tank.pos.x,0,0),size = tank.size, color = color.red)

#turret
turret.theta = rad(45)  
turret.dtheta = rad(1)
turret.L = 3
turret.axis = turret.L*vector(cos(turret.theta),sin(turret.theta),0)

#bullets
bulletsList=[]
m=1
muzzlespeed=15
dspeed=1

#Bar
angleBar.axis = (5*turret.theta)*vector(1,0,0)
speedBar.axis = (muzzlespeed/2.+0.5)*vector(1,0,0) 
make_label(-20,17,
           """Click mouse to start,
Up/Down arrow to raise/lower turret,
Right/Left arrow to speed up/down bullet.""")
  
#motion
g=vector(0,-9.8,0)
dt = 0.01
t = 0
lbl = make_label(0.75*target.pos.x, 0.75 * target.pos.y)
hit = False

scene.bind('keydown', key_ctrl)
while True:
    scene.waitfor('click')#Need a mouse click to continue
    hit = False
    lbl.text = ""
    turret.theta = rad(45)  
    turret.axis = turret.L*vector(cos(turret.theta),sin(turret.theta),0)
    angleBar.axis = (5*turret.theta)*vector(1,0,0)
    muzzlespeed=15
    speedBar.axis = (muzzlespeed/2.+0.5)*vector(1,0,0) 

    for thisbullet in bulletsList :
        thisbullet.visible = False
        bulletsList = []
        
    while hit == False :
        rate(100)
        if muzzlespeed>20:
            muzzlespeed = 20
        if muzzlespeed<1:
            muzzlespeed = 1
        if turret.theta>rad(90):
            turret.theta = rad(90)
        if turret.theta<0:
            turret.theta = 0 

        for thisbullet in bulletsList:
            
            if(thisbullet.pos.y<ground.pos.y+ground.height/2):
                thisbullet.Fnet=vector(0,0,0)
                thisbullet.v=vector(0,0,0)
                if thisbullet.ptd == False :
                    print("포탄 x 좌표 :", thisbullet.pos.x)
                    thisbullet.ptd = True
                    lbl.text = "실패! 포탄 x 좌표 : {:.3f}".format(thisbullet.pos.x)
                
            elif collisionSphereAndBox(thisbullet, target) :
                thisbullet.Fnet = vector(0,0,0)
                thisbullet.v = vector(0,0,0)
                lbl.text = "Boom! 포탄 x 좌표 : {:.3f}".format(thisbullet.pos.x)
                hit = True
                print("포탄 x 좌표 :", thisbullet.pos.x)
                break
                
            else:
                thisbullet.Fnet=m*g
                thisbullet.v += thisbullet.Fnet/m *dt
                thisbullet.pos += dt* thisbullet.v
        t=t+dt