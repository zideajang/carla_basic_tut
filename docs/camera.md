

## 课程内容

- 提供丰富的传感器数据 (摄像头、激光雷达、雷达、IMU等)
- 介绍如何获取摄像头数据

#### 1. 连接到CARLA服务器 

* **代码讲解：**
    ```python
    import carla # 导入CARLA库
    client = carla.Client('localhost',2000) # 创建CARLA客户端，连接本地2000端口
    world = client.get_world() # 获取当前加载的世界对象
    ```
* **要点：**
    * 确保CARLA服务器已在后台运行。
    * `client` 对象是与CARLA模拟器交互的入口。
    * `world` 对象代表模拟环境，可以从中获取地图、参与者等信息。
* **实践环节：**
    * 启动CARLA模拟器。
    * 运行上述代码片段，确认能成功连接并打印 `world` 对象信息。

---

#### 2. 设定车辆与设置视角

* **代码讲解：**
    ```python
    bp_lib = world.get_blueprint_library() # 获取蓝图库
    spawn_points = world.get_map().get_spawn_points() # 获取地图上的出生点
    vehicle_bp = bp_lib.find('vehicle.tesla.model3') # 查找车辆蓝图
    vehicle = world.try_spawn_actor(vehicle_bp,random.choice(spawn_points)) # 在随机出生点生成车辆

    spectator = world.get_spectator() # 获取观察者对象
    # 设置观察者视角跟随车辆，并向后上方偏移
    transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-4,z=2.5)))
    spectator.set_transform(transform) # 应用观察者变换
    ```
* **要点：**
    * **蓝图 (Blueprint)** 是在CARLA中创建对象的模板。
    * **出生点 (Spawn Points)** 是地图中可以安全生成车辆的位置。
    * **`try_spawn_actor`** 尝试生成参与者，如果失败会返回None。
    * **观察者 (Spectator)** 用于控制模拟器中的视角，方便观察。
    * `vehicle.get_transform()` 获取车辆的当前位置和姿态。
* **实践环节：**
    * 在CARLA窗口中观察车辆是否成功生成。
    * 尝试修改 `spectator` 的 `x` 和 `z` 值，观察视角变化。

---

#### 3. 添加摄像头传感器并获取数据

* **代码讲解：**
    ```python
    camera_bp = bp_lib.find('sensor.camera.rgb') # 获取RGB摄像头蓝图
    camera_init_trans = carla.Transform(carla.Location(z=1.6,x=0.4)) # 摄像头相对车辆的初始变换
    camera = world.spawn_actor(camera_bp,camera_init_trans,attach_to=vehicle) # 生成摄像头并附加到车辆

    image_w = camera_bp.get_attribute("image_size_x").as_int() # 获取图像宽度
    image_h = camera_bp.get_attribute("image_size_y").as_int() # 获取图像高度
    camera_data = {'image':np.zeros((image_h,image_w,4))} # 初始化图像数据存储字典

    def camera_cb(image,data_dict): # 定义摄像头回调函数
        data_dict['image'] = np.reshape(np.copy(image.raw_data),(image.height,image.width,4)) # 处理图像数据

    camera.listen(lambda image: camera_cb(image,camera_data)) # 注册监听器，绑定回调函数
    ```
* **要点：**
    * **传感器 (Sensor)** 是获取模拟环境信息的关键。
    * `attach_to` 参数可以将传感器绑定到另一个参与者上，使其随动。
    * **回调函数 (Callback Function)**：当传感器收到数据时，会自动调用注册的回调函数。
    * CARLA提供的原始图像数据是扁平的字节数组，需要使用NumPy进行**重塑 (reshape)**。
    * **`listen()`** 方法开始监听传感器数据流。
* **实践环节：**
    * 运行代码，确认摄像头成功附加到车辆上。
    * 理解 `camera_cb` 函数如何将原始图像数据转换为可用的NumPy数组。

---

#### 4. 实时显示图像与自动驾驶

* **代码讲解：**
    ```python
    vehicle.set_autopilot(True) # 开启车辆自动驾驶
    cv2.imshow('RGB camera',camera_data['image']) # 初始化OpenCV窗口
    while True: # 循环显示图像
        cv2.imshow('RGB camera',camera_data['image']) # 实时更新显示
        if cv2.waitKey(1) == ord('q'): # 按'q'键退出
            break
    ```
* **要点：**
    * `vehicle.set_autopilot(True)` 可以让车辆按照CARLA内置的AI进行驾驶。
    * `cv2.imshow()` 是OpenCV用于显示图像的函数。
    * `cv2.waitKey(1)` 表示等待1毫秒，并捕获按键事件。
    * 循环显示是为了实时更新摄像头画面。
* **实践环节：**
    * 观察CARLA窗口中车辆的自动驾驶行为。
    * 在OpenCV窗口中观察实时摄像头画面。
    * 尝试按 `q` 键退出程序。

---

#### 5. 总结与清理

* **总结：** 回顾本次课程所学内容，强调连接、生成、传感和显示数据的基本流程。
* **清理：** 提醒学生在程序结束后，通常需要销毁创建的参与者，以释放资源。
    * **可选代码片段 (在 `while` 循环结束后添加)：**
        ```python
        # 清理工作
        camera.destroy()
        vehicle.destroy()
        print('Actors destroyed.')
        ```

### 课后练习 (可选)

1.  尝试生成不同类型的车辆或传感器 (例如：激光雷达 `sensor.lidar.ray_cast`)。
2.  修改摄像头参数，如图像分辨率 (`image_size_x`, `image_size_y`) 或视场角 (`fov`)。
3.  尝试控制车辆手动行驶，而不是自动驾驶 (这需要学习 `vehicle.apply_control()` 方法)。
4.  将摄像头图像保存到本地文件。

---
