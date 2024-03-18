# Simulador de Tráfico de Coches

## Integrantes

Ricardo Javier Garza Gámez - A01197496

Pablo Alonso Galvan - A01748288

---

# Proyecto

Este repositorio contiene los archivos necesarios para desarrollar y ejecutar una simulación de tráfico de coches basada en un sistema multiagente. La simulación incluye la modelación de una ciudad en 3D utilizando Unity, la implementación de agentes de tráfico en Python y la conexión entre la simulación en Unity y los agentes en Python mediante una aplicación Node.js.

### El repositorio está organizado de la siguiente manera:

- TrafficSimulator_NodeJS: Contiene los archivos necesarios para la conexión entre Unity y Python mediante una aplicación Node.js.
- TrafficSimulator_Python: Contiene los archivos para la implementación de los agentes de tráfico basados en un sistema multiagente.
- TrafficSimulator_Unity: Contiene los archivos para la modelación de una ciudad en 3D y la visualización de los agentes de tráfico en Unity.

### Cómo Utilizar: 
1. Clona este repositorio en tu máquina local, asegurándote de estar en la rama "FINAL-REVISION" o "main".
2. Accede a la carpeta “TrafficSimulator_NodeJS”, la cual contiene:
   - node_modules: Carpeta que contiene las dependencias del proyecto.
   - index.js: Archivo principal de la aplicación Node.js que establece un servidor WebSocket para la comunicación entre Unity y Python.
   - package-lock.json: Archivo generado automáticamente que especifica las versiones exactas de las dependencias instaladas.
   - package.json: Archivo de configuración del proyecto Node.js que especifica las dependencias del proyecto, scripts y otra información relevante.
Por lo que dentro de esta carpeta se debe correr el index.js
3. Por otro lado, dentro de la carpeta “TrafficSimulator_Python”, conteniendo:
   - Classes: Carpeta que contiene las clases necesarias para la simulación.
   - main.py: Archivo principal que contiene la lógica principal de la simulación de tráfico, incluyendo la definición de las carreteras, controles de curvas, objetivos y generación de vehículos.
Por lo que dentro de esta carpeta se debe correr el main.py
4. Por último, se encuentra “TrafficSimulator_Unity”, que contiene:
   - .vscode: Carpeta que puede contener archivos de configuración específicos para Visual Studio Code.
   - Assets: Carpeta que contiene los assets utilizados en el proyecto de Unity.
   - Packages: Carpeta que puede contener paquetes de Unity utilizados en el proyecto.
   - ProjectSettings: Carpeta que puede contener configuraciones del proyecto de Unity.
   - .vsconfig: Archivo de configuración para Visual Studio Code.
   - A su vez se encuentran los siguientes scripts dentro de la carpeta Assets:
      - CarSpawner: Este script se encarga de generar vehículos en el escenario. Se define una clase `Vehicle` para representar los vehículos, y el método `GenerateVehicle` instancia un vehículo.
      - TrafficLightController: Este script controla el ciclo de luces de los semáforos en el escenario. El método `UpdateLightCycle` cambia entre las luces rojas y verdes de manera cíclica.
      - WebSocketClient: Este script establece una conexión WebSocket con el servidor Node.js para recibir actualizaciones sobre los vehículos y los semáforos. Utiliza la biblioteca WebSocketSharp para la comunicación y actualiza la escena de Unity en consecuencia.

Abre el proyecto Unity contenido en la carpeta `TrafficSimulator_Unity` con Unity Hub, configura las escenas, assets y configuraciones necesarias para tu simulación dentro de Unity. Ejecuta el proyecto en el editor de Unity.
Una vez que la simulación este en ejecución, podrás observar la interacción de los agentes de trafico en la ciudad modelada en 3D.



