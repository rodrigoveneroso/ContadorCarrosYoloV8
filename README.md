# Car Counter

[Clique aqui para a versão em português](#português)

This project uses YOLOv8 for car detection and the SORT algorithm for tracking. It identifies cars and counts them as they cross a predefined line within the video.

## Features
- Car detection and counting using YOLOv8 and SORT from a video.
- Displays the total vehicle count in the top-left corner of the screen.

![Car count demo](car_count_demo.gif)

## Setup

### Installation

1. **Clone the repository**
   ```git clone https://github.com/rodrigoveneroso/ContadorCarrosYoloV8```

2. **Install the dependencies**
    ```pip install -r requirements.txt```

## Usage

1. **Place your video file** in the project directory and name it `car_video.mp4` (or change the `video_file` constant in the code).

2. **Run the detection script**
    ```python main.py```

3. **Exit the program** by pressing the 'q' key while the video window is active.

## How It Works

The logic of this vehicle detection and tracking system is divided into several stages:

1. **Initialization**:
   - The program initializes the video feed, the YOLOv8 model, and the SORT tracker.
   - It loads a mask image to analyze only specific regions of interest in the video (used in the demonstration to avoid capturing cars going in the opposite direction).

2. **Object Detection**:
   - Each video frame is processed using the YOLOv8 model.
   - The model identifies objects in the frame, and detections are filtered to consider only cars, trucks, and buses.

3. **Object Tracking**:
   - The SORT algorithm is used to assign unique IDs to detected vehicles and track their positions across multiple frames.
   - Through tracking, it is possible to prevent the same car from being counted more than once.

4. **Detection Line**:
   - A horizontal line is drawn on the video frame.
   - As each vehicle crosses this line, the system checks its position and ensures that it is counted only once.

5. **Vehicle Counting**:
   - When a vehicle crosses the detection line, its unique ID is stored to avoid duplicate counts.
   - The total number of vehicles is displayed in real-time on the video feed.

6. **Logging and Output**:
   - The system logs all significant events, such as when a vehicle is counted or if there are problems reading the video file.
   - The output video with bounding boxes and the total vehicle count is displayed in a window.

---

# [PORTUGUÊS]

# Contador de Carros
Este projeto utiliza o YOLOv8 para a detecção de carros e o algoritmo SORT para o rastreamento. Ele identifica carros e os conta ao cruzarem uma linha predefinida dentro do video.

## Funcionalidades
- Detecção e contagem de carros usando YOLOv8 e SORT a partir de um video.
- Exibe a contagem total de veículos no canto superior esquerdo da tela.

![Car count demo](car_count_demo.gif)

## Configuração

### Instalação

1. **Clone o repositório**
   ```git clone https://github.com/rodrigoveneroso/ContadorCarrosYoloV8```

2. **Instale as dependências**
    ```pip install -r requirements.txt```

## Uso

1. **Coloque seu arquivo de vídeo** no diretório do projeto e nomeie como `car_video.mp4` (ou altere a constante `video_file` no código).

2. **Execute o script de detecção**
    ```python main.py```

3. **Encerre o programa** pressionando a tecla 'q' enquanto a janela de vídeo estiver ativa.

## Como Funciona

A lógica deste sistema de detecção e rastreamento de veículos é dividida em várias etapas:

1. **Inicialização**:
   - O programa inicializa o feed de vídeo, o modelo YOLOv8 e o rastreador SORT.
   - Ele carrega uma imagem de máscara para analisar somente uma região específica de interesse no vídeo (no caso da demonstração, foi utilizado para não captar os carros na contramão).

2. **Detecção de Objetos**:
   - Cada frame do vídeo é processado usando o modelo YOLOv8.
   - O modelo identifica objetos no frame e são filtradas as detecções para considerar apenas carros, caminhões e ônibus.

3. **Rastreamento de Objetos**:
   - O algoritmo SORT é usado para atribuir IDs únicos aos veículos detectados e rastrear suas posições em múltiplos frames.
   - Por meio do rastreamento, é possível evitar que o mesmo carro seja contado mais de uma vez.

4. **Linha de Detecção**:
   - Uma linha horizontal é desenhada no quadro de vídeo.
   - À medida que cada veículo cruza essa linha, o sistema verifica sua posição e garante que ele seja contado apenas uma vez.

5. **Contagem de Veículos**:
   - Quando um veículo cruza a linha de detecção, seu ID único é armazenado para evitar contagens duplicadas.
   - O número total de veículos é exibido em tempo real no feed de vídeo.

6. **Logging e Saída**:
   - O sistema registra todos os eventos significativos, como quando um veículo é contado ou se há problemas na leitura do arquivo de vídeo.
   - O vídeo de saída com as caixas delimitadoras e a contagem total de veículos é exibido em uma janela.
