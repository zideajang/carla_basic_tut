import carla
import math
import random
import time
import numpy as np
import cv2


# 连接到CARLA服务器
client = carla.Client('localhost',2000)
# 示例：加载Town01地图
# world = client.load_world('Town01')
 # 示例：卸载停车车辆层
# world.unload_map_layer(carla.MapLayer.ParkedVehicles)
# 获取当前加载的CARLA世界对象
world = client.get_world()


# 获取世界(world)中所有的角色（actors），包括静态和动态的
static_objects = world.get_actors()

# for obj in static_objects:
#     if obj.type_id not in ['vehicle.tesla.model3', 'static.prop.road']:
#         print(dir(obj))
#         obj.destroy()

# 获取蓝图库，用于创建各种CARLA对象
bp_lib = world.get_blueprint_library()
# 获取可以初始化车辆的位置，即地图的出生点
spawn_points = world.get_map().get_spawn_points()

# 获取观察者（旁观者）对象，用于控制视角
spectator = world.get_spectator()

# 选择车辆类型蓝图, 这里选择的是特斯拉的 model3 
vehicle_bp = bp_lib.find('vehicle.tesla.model3')
# 尝试在随机选择的出生点生成一辆车
vehicle = world.try_spawn_actor(vehicle_bp,random.choice(spawn_points))

spectator = world.get_spectator()
transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-4,z=2.5)))
spectator.set_transform(transform)

camera_bp = bp_lib.find('sensor.camera.rgb')
camera_init_trans = carla.Transform(carla.Location(z=1.6,x=0.4))
camera = world.spawn_actor(camera_bp,camera_init_trans,attach_to=vehicle)

world.on_tick(lambda world_snapshot: print(world_snapshot))
# 
# actor_list = world.get_actors()
# for actor in actor_list:
#     print(actor.type_id)


# step one
# time.sleep(0.2)
# spectator.set_transform(camera.get_transform())
# camera.destroy()
# 获取摄像头图像的宽度和高度
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()

# 初始化一个字典来存储摄像头数据，预先分配一个全零的NumPy数组用于图像
camera_data = {'image':np.zeros((image_h,image_w,4))}

# 定义摄像头回调函数
def camera_cb(image,data_dict):
    data_dict['image'] = np.reshape(np.copy(image.raw_data),(image.height,image.width,4))
# 监听摄像头数据流，当有新图像时调用camera_cb函数
camera.listen(lambda image: camera_cb(image,camera_data))
# 将车辆设置为自动驾驶模式
vehicle.set_autopilot(True)


# 在OpenCV窗口中显示摄像头图像
cv2.imshow('RGB camera',camera_data['image'])
while True:
    cv2.imshow('RGB camera',camera_data['image'])

    if cv2.waitKey(1) == ord('q'):
        break





