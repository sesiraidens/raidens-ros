<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" width="80">

# raidens-ros

Nodes e configuracoes ROS2 para robos autônomos da RAIDENS.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![ROS2](https://img.shields.io/badge/ROS2-Humble-22313E?style=flat)
![License](https://img.shields.io/badge/License-MIT-d9333b?style=flat)
![Status](https://img.shields.io/badge/Status-Active-2ea043?style=flat)

</div>

---

## Sobre

O **raidens-ros** fornece uma estrutura base para integrar robos da RAIDENS com ROS2 (Robot Operating System 2). Inclui nodes, topics e geradores de launch.

---

## Estrutura

`
raidens-ros/
├── src/
│   ├── nodes.py          # Nodes ROS2
│   └── __init__.py
├── examples/
│   ├── launch_arquivo.py
│   └── testar_nodes.py
└── README.md
`

---

## Nodes

### NodeSensores

Leitura e publicacao de dados de sensores.

`python
from src.nodes import NodeSensores

node = NodeSensores()

# Publicar dados
node.publicar_ultrassonico(30.5)  # 30.5cm
node.publicar_imu([0, 0, 9.8], [0, 0, 0])
node.publicar_ir([0, 1, 0, 1, 0])
`

**Topics:**
- /sensor/ultrassonico - Distancia (Range)
- /sensor/imu - Aceleracao e giroscopio (Imu)
- /sensor/ir - Sensores de linha (Int32MultiArray)

### NodeMotores

Controle de motores e odometria.

`python
from src.nodes import NodeMotores

node = NodeMotores()
node.receber_comando(0.3, 0.0)  # 0.3 m/s, sem rotacao
node.publicar_odometria(posicao, orientacao)
`

**Topics:**
- /cmd_vel - Comando de velocidade (Twist)
- /motor/odometry - Odometria (Odometry)

### NodeNavegacao

Planejamento e seguimento de rota.

`python
from src.nodes import NodeNavegacao

node = NodeNavegacao()
node.definir_parametro("velocidade_maxima", 0.5)
node.planear_rota(destino)
node.seguir_rota(rota)
`

**Topics:**
- /navegacao/destino - Destino (PoseStamped)
- /navegacao/rota - Rota planejada (Path)

### NodeVisao

Processamento de imagem e deteccao.

`python
from src.nodes import NodeVisao

node = NodeVisao()
node.processar_frame(frame)
node.publicar_deteccoes(deteccoes)
`

**Topics:**
- /camera/image_raw - Imagem da camera (Image)
- /visao/deteccoes - Deteccoes (Detection2DArray)

---

## Topics Padrao

`python
from src.nodes import TopicosPadrao

todos = TopicosPadrao.listar_todos()
for nome, topico in todos.items():
    print(f"{nome}: {topico}")
`

| Categoria | Topic | Tipo |
|---|---|---|
| Ultrassonico | /sensor/ultrassonico | Range |
| IMU | /sensor/imu | Imu |
| IR | /sensor/ir | Int32MultiArray |
| Camera | /camera/image_raw | Image |
| Comando | /cmd_vel | Twist |
| Odometria | /motor/odometry | Odometry |

---

## Gerar Launch

`python
from src.nodes import ConfiguracaoROS, NodeSensores, NodeMotores

config = ConfiguracaoROS()
config.adicionar_node(NodeSensores())
config.adicionar_node(NodeMotores())

config.gerar_launch("launch/raidens_launch.py")
config.gerar_pkg_xml("package.xml")
`

---

## Instalacao ROS2

`ash
# Instalar ROS2 Humble
sudo apt install ros-humble-desktop

# Instalar pacotes adicionais
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-vision-msgs
`

---

## Equipe

**RAIDENS - SESI Aluminio 192**

Desenvolvido para uso interno da equipe. Licenciado sob MIT.