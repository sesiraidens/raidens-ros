"""
Modulo ROS (Robot Operating System) para robotica.

Contem nodes, topics e configuracoes para integracao
com ROS2 em robos da RAIDENS.
"""


class NodeBase:
    """
    Classe base para nodes ROS2.
    """
    
    def __init__(self, nome, namespace="/"):
        self.nome = nome
        self.namespace = namespace
        self.topics = {}
        self parametros = {}
        
    def criar_topic(self, nome, tipo):
        """Registra um topic."""
        self.topics[nome] = {
            "tipo": tipo,
            "inscrito": False,
            "publicado": False
        }
        
    def publicar(self, nome, mensagem):
        """Publica mensagem em um topic."""
        if nome in self.topics:
            print(f"[{self.nome}] Publicando em {nome}: {mensagem}")
            
    def receber(self, nome, callback):
        """Inscreve em um topic."""
        if nome in self.topics:
            self.topics[nome]["inscrito"] = True
            print(f"[{self.nome}] Inscrito em {nome}")
            
    def definir_parametro(self, nome, valor):
        """Define um parametro."""
        self.parametros[nome] = valor
        
    def obter_parametro(self, nome, padrao=None):
        """Obtem um parametro."""
        return self.parametros.get(nome, padrao)


class NodeSensores(NodeBase):
    """
    Node para leitura de sensores.
    """
    
    def __init__(self):
        super().__init__("node_sensores")
        
        self.criar_topic("/sensor/ultrassonico", "sensor_msgs/msg/Range")
        self.criar_topic("/sensor/imu", "sensor_msgs/msg/Imu")
        self.criar_topic("/sensor/ir", "std_msgs/msg/Int32MultiArray")
        
    def publicar_ultrassonico(self, distancia):
        """Publica distancia do ultrassonico."""
        self.publicar("/sensor/ultrassonico", {
            "range": distancia,
            "min_range": 0.02,
            "max_range": 4.0,
            "field_of_view": 0.26
        })
        
    def publicar_imu(self, aceleracao, giroscopio):
        """Publica dados do IMU."""
        self.publicar("/sensor/imu", {
            "linear_acceleration": aceleracao,
            "angular_velocity": giroscopio
        })
        
    def publicar_ir(self, leituras):
        """Publica leituras dos sensores IR."""
        self.publicar("/sensor/ir", {"data": leituras})


class NodeMotores(NodeBase):
    """
    Node para controle de motores.
    """
    
    def __init__(self):
        super().__init__("node_motores")
        
        self.criar_topic("/cmd_vel", "geometry_msgs/msg/Twist")
        self.criar_topic("/motor/odometry", "nav_msgs/msg/Odometry")
        
    def receber_comando(self, velocidade_linear, velocidade_angular):
        """Recebe comando de velocidade."""
        self.parametros["vel_linear"] = velocidade_linear
        self.parametros["vel_angular"] = velocidade_angular
        
    def publicar_odometria(self, posicao, orientacao):
        """Publica odometria."""
        self.publicar("/motor/odometry", {
            "pose": {"position": posicao, "orientation": orientacao},
            "twist": {"linear": {"x": 0}, "angular": {"z": 0}}
        })


class NodeNavegacao(NodeBase):
    """
    Node para navegacao autonoma.
    """
    
    def __init__(self):
        super().__init__("node_navegacao")
        
        self.criar_topic("/navegacao/destino", "geometry_msgs/msg/PoseStamped")
        self.criar_topic("/navegacao/rota", "nav_msgs/msg/Path")
        
        self.definir_parametro("velocidade_maxima", 0.5)
        self.definir_parametro("distancia_seguranca", 0.3)
        
    def planear_rota(self, destino):
        """Planeja rota ate destino."""
        print(f"[{self.nome}] Planejando rota ate {destino}")
        
    def seguir_rota(self, rota):
        """Segue uma rota."""
        print(f"[{self.nome}] Seguindo rota com {len(rota)} pontos")


class NodeVisao(NodeBase):
    """
    Node para processamento de imagem.
    """
    
    def __init__(self):
        super().__init__("node_visao")
        
        self.criar_topic("/camera/image_raw", "sensor_msgs/msg/Image")
        self.criar_topic("/visao/deteccoes", "vision_msgs/msg/Detection2DArray")
        
    def processar_frame(self, frame):
        """Processa frame da camera."""
        print(f"[{self.nome}] Processando frame {frame.shape}")
        
    def publicar_deteccoes(self, deteccoes):
        """Publica deteccoes encontradas."""
        self.publicar("/visao/deteccoes", {"detections": deteccoes})


class ConfiguracaoROS:
    """
    Configuracao para launch files do ROS2.
    """
    
    def __init__(self):
        self.nodes = {}
        self.topics = {}
        self.params = {}
        
    def adicionar_node(self, node):
        """Adiciona um node a configuracao."""
        self.nodes[node.nome] = node
        
    def gerar_launch(self, caminho):
        """Gera arquivo launch.py."""
        codigo = """# Launch file gerado por raidens-ros
# RAIDENS - SESI 192

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
"""
        for nome, node in self.nodes.items():
            codigo += f"""        Node(
            package='raidens_ros',
            executable='{nome}',
            name='{nome}',
            namespace='{node.namespace}'
        ),
"""
        
        codigo += """    ])
"""
        
        with open(caminho, 'w') as f:
            f.write(codigo)
        print(f"Launch file gerado: {caminho}")
        
    def gerar_pkg_xml(self, caminho):
        """Gera package.xml."""
        codigo = """<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xerd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>raidens_ros</name>
  <version>1.0.0</version>
  <description>Pacote ROS para robos RAIDENS</description>
  <maintainer email="raidens@sesi.edu.br">RAIDENS</maintainer>
  <license>MIT</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>vision_msgs</depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
"""
        
        with open(caminho, 'w') as f:
            f.write(codigo)
        print(f"package.xml gerado: {caminho}")


class TopicosPadrao:
    """
    Topics padrao para robos da RAIDENS.
    """
    
    SENSORES = {
        "ultrassonico": "/sensor/ultrassonico",
        "imu": "/sensor/imu",
        "ir": "/sensor/ir",
        "camera": "/camera/image_raw",
        "encoder": "/sensor/encoder"
    }
    
    MOTORES = {
        "comando": "/cmd_vel",
        "odometria": "/motor/odometry"
    }
    
    NAVEGACAO = {
        "destino": "/navegacao/destino",
        "rota": "/navegacao/rota",
        "mapa": "/map"
    }
    
    VISAO = {
        "imagem": "/camera/image_raw",
        "deteccoes": "/visao/deteccoes"
    }
    
    @classmethod
    def listar_todos(cls):
        """Lista todos os topics padrao."""
        todos = {}
        todos.update(cls.SENSORES)
        todos.update(cls.MOTORES)
        todos.update(cls.NAVEGACAO)
        todos.update(cls.VISAO)
        return todos






