using UnityEngine;
using WebSocketSharp;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System;

[System.Serializable]
public class VehicleData
{
    public string id;
    public float x;
    public float y;
    public float heading;
}

public class WebSocketClient : MonoBehaviour
{
    CarSpawner carSpawner;
    TrafficLightController trafficController;
    WebSocket ws; 

    private readonly ConcurrentQueue<Action> _actions = new ConcurrentQueue<Action>();

    private void Start()
    {   
        
        carSpawner = GameObject.FindGameObjectWithTag("CarSpawner").GetComponent<CarSpawner>();
        trafficController = GameObject.FindGameObjectWithTag("TrafficController").GetComponent<TrafficLightController>();

        ws = new WebSocket("ws://localhost:1123/?uid=unity_client");
        ws.OnMessage += (sender, e) => {

            Dictionary<string, object> jsonDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(e.Data);

            string action_json = jsonDict["action"].ToString();

            switch (action_json){
                case "add_vehicle":
                    var dataObject_add = jsonDict["data"];
                    var vehicleData_add = JsonConvert.DeserializeObject<VehicleData>(dataObject_add.ToString());
                    string vehicleId_add = vehicleData_add.id;

                    _actions.Enqueue(() => carSpawner.GenerateVehicle(vehicleId_add));
                    break;
                case "remove_vehicle":
                    var dataObject_remove = jsonDict["data"];
                    var vehicleData_remove = JsonConvert.DeserializeObject<VehicleData>(dataObject_remove.ToString());
                    string vehicleId_remove= vehicleData_remove.id;

                    _actions.Enqueue(() => carSpawner.DeleteVehicle(vehicleId_remove));
                    break;
                case "update_vehicles":
                    List<VehicleData> dataList = JsonConvert.DeserializeObject<List<VehicleData>>(jsonDict["data"].ToString());

                    foreach (VehicleData data in dataList){
                        _actions.Enqueue(() => carSpawner.updateVehicle(data.id, data.x, data.y, data.heading));
                    }

                    break;
                case "update_lights_cycle":
                    _actions.Enqueue(() => trafficController.UpdateLightCycle());
                    break;
                default:
                    Debug.LogError("Unknown action: " + action_json);
                    break;
            }
        };
        ws.Connect();
    }

    private void Update ()
    {
        // Work the dispatched actions on the Unity main thread
        while(_actions.Count > 0)
        {
            if(_actions.TryDequeue(out var action))
            {
                action?.Invoke();
            }
        }
    }
}