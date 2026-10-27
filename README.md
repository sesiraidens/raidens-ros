<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="140">

# raidens-ros

**Estrutura de nodes e tópicos ROS 2 para os robôs autônomos da RAIDENS**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?style=flat-square&logo=ros&logoColor=white)
![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-D9333B?style=flat-square)

[Sobre](#sobre) · [Instalação](#instalação) · [Nodes](#nodes) · [Tópicos](#tópicos-padrão) · [Launch](#gerando-launch-e-packagexml)

</div>

---

## Sobre

O **raidens-ros** é o ponto de partida da equipe para migrar os robôs para o ROS 2. Ele define, em Python puro, quais nodes o robô terá, quais tópicos cada um publica e assina e com quais tipos de mensagem. A partir disso, gera o `launch.py` e o `package.xml` do pacote.

Com o desenho da arquitetura separado da implementação, a equipe pode discutir e revisar a comunicação entre as partes do robô antes de escrever código dependente do `rclpy`.

## Instalação

```bash
git clone https://github.com/sesiraidens/raidens-ros.git
cd raidens-ros
```

Para executar os pacotes gerados, instale o ROS 2 Humble:

```bash
sudo apt install ros-humble-desktop
sudo apt install ros-humble-nav2-bringup ros-humble-vision-msgs
```

## Nodes

| Node | Responsabilidade | Principais métodos |
|---|---|---|
| `NodeSensores` | Publica leituras dos sensores | `publicar_ultrassonico`, `publicar_imu`, `publicar_ir` |
| `NodeMotores` | Recebe comandos de velocidade e publica odometria | `receber_comando`, `publicar_odometria` |
| `NodeNavegacao` | Planeja e segue rotas | `planear_rota`, `seguir_rota` |
| `NodeVisao` | Processa a câmera e publica detecções | `processar_frame`, `publicar_deteccoes` |

Todos herdam de `NodeBase`, que oferece `criar_topic`, `publicar`, `receber`, `definir_parametro` e `obter_parametro`.

```python
from src.nodes import NodeSensores, NodeMotores

sensores = NodeSensores()
sensores.publicar_ultrassonico(30.5)        # cm
sensores.publicar_ir([0, 1, 0, 1, 0])

motores = NodeMotores()
motores.receber_comando(0.3, 0.0)           # 0,3 m/s, sem rotação
```

## Tópicos padrão

| Categoria | Tópico | Tipo |
|---|---|---|
| Ultrassônico | `/sensor/ultrassonico` | `Range` |
| IMU | `/sensor/imu` | `Imu` |
| IR | `/sensor/ir` | `Int32MultiArray` |
| Câmera | `/camera/image_raw` | `Image` |
| Detecções | `/visao/deteccoes` | `Detection2DArray` |
| Comando | `/cmd_vel` | `Twist` |
| Odometria | `/motor/odometry` | `Odometry` |
| Destino | `/navegacao/destino` | `PoseStamped` |
| Rota | `/navegacao/rota` | `Path` |

A lista completa fica em `TopicosPadrao.listar_todos()`.

## Gerando launch e package.xml

```python
from src.nodes import ConfiguracaoROS, NodeSensores, NodeMotores

config = ConfiguracaoROS()
config.adicionar_node(NodeSensores())
config.adicionar_node(NodeMotores())

config.gerar_launch("launch/raidens_launch.py")
config.gerar_pkg_xml("package.xml")
```

## Estrutura

```text
raidens-ros/
└── src/
    └── nodes.py   # Nodes, tópicos padrão e gerador de launch
```

## Ecossistema RAIDENS

Este repositório faz parte de um conjunto de bibliotecas da equipe. Elas usam os mesmos nomes de classes e convenções, então o que você aprende em uma serve nas outras.

| Repositório | Para quê |
|---|---|
| [`raidens-python`](https://github.com/sesiraidens/raidens-python) | Biblioteca principal em Python: sensores, motores e robôs prontos (seguidor, parede, resgate) |
| [`raidens-arduino`](https://github.com/sesiraidens/raidens-arduino) | As mesmas abstrações em C++ para rodar direto no Arduino |
| [`raidens-sensores`](https://github.com/sesiraidens/raidens-sensores) | Catálogo completo de sensores com calibração e filtragem |
| [`raidens-motores`](https://github.com/sesiraidens/raidens-motores) | Motores DC, servo, passo, driver L298N e rodas mecanum |
| [`raidens-pid`](https://github.com/sesiraidens/raidens-pid) | Controladores PID, PID avançado, cascata e sintonia Ziegler-Nichols |
| [`raidens-opencv`](https://github.com/sesiraidens/raidens-opencv) | Visão computacional: cores, linhas e navegação por câmera |
| [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) | Calibração interativa de cores em HSV e LAB |
| [`raidens-obr`](https://github.com/sesiraidens/raidens-obr) | Robô completo para a OBR, integrando sensores, motores e missões |
| [`raidens-electronics`](https://github.com/sesiraidens/raidens-electronics) | Cálculos e modelos de componentes eletrônicos |
| [`raidens-3d`](https://github.com/sesiraidens/raidens-3d) | Peças 3D paramétricas geradas em OpenSCAD |
| [`raidens-snippets`](https://github.com/sesiraidens/raidens-snippets) | Trechos de código prontos para copiar e colar |

---

<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="56">

**Equipe RAIDENS** · SESI 192 Alumínio/SP

[![Email](https://img.shields.io/badge/Email-sesiraidens%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:sesiraidens@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-sesiraidens-39E06B?style=flat-square&logo=linktree&logoColor=white)](https://linktr.ee/sesiraidens)
[![GitHub](https://img.shields.io/badge/GitHub-sesiraidens-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/sesiraidens)

<sub>Desenvolvido pela equipe RAIDENS para fins educacionais. Licenciado sob MIT.</sub>

</div>


